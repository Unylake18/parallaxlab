"""yt_0013 — Colisões em 1D: como saber o que acontece depois? (Física I · Mecânica · Colisões) — v2.

Cena completa SILENCIOSA C01–C12, inteiramente em Manim 2D/2.5D (sem Blender; ver direcao_v2.md).
Preview 960×540 / 15 fps:
    uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0013_colisoes_1d/cena.py Colisoes1DYT013
Trecho isolado (desenvolvimento): SECOES=c06,c07 (cada seção reconstrói o estado de que precisa).

Cores: corpo 1 azul · corpo 2 violeta · vetores físicos branco · K e resultado ativo ciano ·
energia convertida em interna magenta · U_g violeta claro. Sem laranja/amarelo.
Notação: u velocidade antes, v depois, índices 1/2 = corpos, +x à direita; pêndulo: m, M, u, V, h, estados A/B/C.
Um único estado físico alimenta posição, setas, barras e gráficos (relógio físico = ValueTracker).
"""
import os
import sys
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402

# ── paleta (local do v2) ─────────────────────────────────────────────────────────────────────────────────────
WHITE_ = TEXT_COLOR
CYAN = PRIMARY_COLOR        # K e resultado ativo
C1F, C1 = "#267BFF", "#4D93FF"      # corpo 1: preenchimento / símbolos
C2F, C2 = "#745CFF", "#9C8CFF"      # corpo 2
MAG = "#EA63FF"             # parcela convertida em energia interna
UG = "#9C8CFF"              # energia potencial gravitacional (sempre com rótulo U_g)
STEEL = "#6F7C92"
DIM = "#8FA3C4"
GREY = "#B8C4DA"

SECOES = [s.strip() for s in os.environ.get("SECOES", "").split(",") if s.strip()]
AUDITORIA = os.environ.get("AUDITORIA") == "1"   # mede sobreposições de texto em cada pausa (desenvolvimento)

# 960×540: texto principal ~22–24 px, rótulos ~15–17 px, matemática central ~29–33 px (medido)
T_MAIN, T_LAB, T_SMALL = 38, 27, 24
M_MAIN, M_MID, M_REF, M_LAB = 66, 56, 46, 40

TOK = {}
for _s in ("m_1", "u_1", "v_1", "u_1^2", "v_1^2", "p_1", "K_1"):
    TOK[_s] = C1
for _s in ("m_2", "u_2", "v_2", "u_2^2", "v_2^2", "p_2", "K_2"):
    TOK[_s] = C2
for _s in ("K_i", "K_f", "K_A", "K_B", "K_C"):
    TOK[_s] = CYAN
for _s in ("U_g", "U_B", "U_C"):
    TOK[_s] = UG

# Exemplo-base (C01–C03): m1 = 2 kg, m2 = 1 kg, u1 = +2 m/s, u2 = −2 m/s; P = +2 kg·m/s nos três desfechos
BASE = (2.0, 1.0, 2.0, -2.0)
FINAIS = (("rebatem", -2 / 3, 10 / 3), ("se separam", 0.0, 2.0), ("ficam juntos", 2 / 3, 2 / 3))

# Pêndulo balístico (modelo interno): m = 20 g, M = 980 g, L = 1,0 m, g = 9,8 m/s², h = 0,20 m
PM, PMM, PL, PG, PH = 0.020, 0.980, 1.0, 9.8, 0.20
PV = np.sqrt(2 * PG * PH)                 # ≈ 1,980 m/s
PU = (PM + PMM) / PM * PV                 # ≈ 98,99 m/s
ESC = 3.0                                 # unidades de tela por metro (pêndulo)


def _subida():
    """Integra θ'' = −(g/L) sen θ (sem dissipação) de θ = 0, ω = V/L até ω = 0 (RK4)."""
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


def txt(s, size=T_MAIN, color=WHITE_, op=1.0):
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)


def M(*parts, size=M_MAIN, color=WHITE_, w=None):
    """MathTex por partes (TransformMatchingTex casa partes); termos do corpo 1 azuis e do corpo 2 violeta."""
    m = MathTex(*parts, font_size=size, color=color, tex_to_color_map=TOK)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    return m


def P3(x, y):
    return np.array([x, y, 0.0])


def arrow(a, b, color=WHITE_, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def box(m, color=CYAN, buff=0.12, width=3):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.08)


def contorno(m, buff=0.3, color=GREY):
    r = RoundedRectangle(corner_radius=0.18, width=m.width + 2 * buff, height=m.height + 2 * buff).move_to(m)
    return DashedVMobject(r.set_stroke(color, 2.2), num_dashes=60)


def barra(x0, y, largura, cor, h=0.34, op=0.9):
    r = Rectangle(width=max(largura, 1e-3), height=h, stroke_width=0, fill_color=cor, fill_opacity=op)
    return r.move_to(P3(x0 + max(largura, 1e-3) / 2, y))


class Corpo(VGroup):
    """Corpo 2.5D: face frontal (referência de medidas e contatos) + faces superior/lateral decorativas."""

    def __init__(self, nome, cf, cs, lado, size=40, alt=None):
        super().__init__()
        alt = alt or lado
        self.lado, self.alt = lado, alt
        f = RoundedRectangle(corner_radius=0.05, width=lado, height=alt, stroke_color=cs, stroke_width=3,
                             fill_color=cf, fill_opacity=0.45)
        D = np.array([0.13, 0.09, 0.0])
        ul, ur, dr = f.get_corner(UL), f.get_corner(UR), f.get_corner(DR)
        top = Polygon(ul, ul + D, ur + D, ur, stroke_color=cs, stroke_width=1.2, stroke_opacity=0.7, fill_color=cf,
                      fill_opacity=0.25)
        side = Polygon(ur, ur + D, dr + D, dr, stroke_color=cs, stroke_width=1.2, stroke_opacity=0.7, fill_color=cf,
                       fill_opacity=0.14)
        self.front = f
        self.add(side, top, f)
        if nome:
            self.lab = MathTex(nome, font_size=size, color=WHITE_).move_to(f)
            self.add(self.lab)

    def at(self, x, yb):
        """Centro da face frontal em x, base em yb."""
        self.shift(P3(x, yb + self.alt / 2) - self.front.get_center())
        return self


class Col:
    """Colisão 1D com contato instantâneo em xc no instante t = 0 (t = relógio físico, em s; kx = tela por metro)."""

    def __init__(self, m1, m2, u1, u2, v1, v2, w1=1.0, w2=1.0, xc=0.0, ty=-1.6, kx=0.9, ka=0.5, t0=-1.5,
                 n1="m_1", n2="m_2", pre=("u_1", "u_2"), post=("v_1", "v_2"), junto=None, lab=M_LAB, nsize=40,
                 eixo=True, trilho=(-7.3, 7.3)):
        self.m1, self.m2, self.u1, self.u2, self.v1, self.v2 = m1, m2, u1, u2, v1, v2
        self.w1, self.w2, self.xc, self.ty, self.kx, self.ka = w1, w2, xc, ty, kx, ka
        self.pre, self.post, self.junto = pre, post, junto
        self.t, self.ao = ValueTracker(t0), ValueTracker(1.0)
        self.b1, self.b2 = Corpo(n1, C1F, C1, w1, size=nsize), Corpo(n2, C2F, C2, w2, size=nsize)
        self.b1.add_updater(lambda m: m.at(self.x1(), ty))
        self.b2.add_updater(lambda m: m.at(self.x2(), ty))
        self.b1.at(self.x1(), ty)
        self.b2.at(self.x2(), ty)
        self.track = VGroup(Line(P3(trilho[0], ty), P3(trilho[1], ty), color=STEEL, stroke_width=3))
        if eixo:
            ax = arrow(P3(trilho[1] - 1.4, ty - 0.42), P3(trilho[1] - 0.4, ty - 0.42), color=GREY, width=3, tip=0.16)
            self.track.add(ax, MathTex("+x", font_size=34, color=GREY).next_to(ax, LEFT, buff=0.12))
        names = [n for n in (*pre, *post, junto) if n]
        self.L = {n: M(n, size=lab) for n in names}
        self.arrows = always_redraw(self._arrows)

    def vel(self):
        return (self.v1, self.v2) if self.t.get_value() > 1e-6 else (self.u1, self.u2)

    def x1(self):
        return self.xc - self.w1 / 2 + self.vel()[0] * self.t.get_value() * self.kx

    def x2(self):
        return self.xc + self.w2 / 2 + self.vel()[1] * self.t.get_value() * self.kx

    def _vec(self, x, y, vel, name):
        """name: texto do rótulo; None = seta sem rótulo; False = nada."""
        if name is False:
            return VGroup()
        L = vel * self.ka
        base = P3(x, y)
        lab = self.L.get(name) if name else None
        if abs(L) < 0.06:
            return VGroup(lab.move_to(base + UP * 0.2)) if lab else VGroup()
        a = arrow(base, base + RIGHT * L, width=6, tip=0.22)
        g = VGroup(a)
        if lab:
            g.add(lab.next_to(a, UP, buff=0.08))
        return g

    def _arrows(self):
        op = self.ao.get_value()
        if op <= 0.01:
            return VGroup()
        t = self.t.get_value()
        y0 = self.ty + 0.3
        if t > 1e-6 and self.junto is not None:
            xm = (self.x1() + self.x2()) / 2
            g = VGroup(self._vec(xm, y0 + max(self.w1, self.w2), self.v1, self.junto or None))
        else:
            n1, n2 = self.post if t > 1e-6 else self.pre
            v1, v2 = self.vel()
            g = VGroup(self._vec(self.x1(), y0 + self.w1, v1, n1), self._vec(self.x2(), y0 + self.w2, v2, n2))
        return g.set_opacity(op)

    def group(self, arrows=True):
        return VGroup(self.track, self.b1, self.b2, *([self.arrows] if arrows else []))

    def contato(self):
        return Flash(P3(self.xc, self.ty + 0.5 * min(self.w1, self.w2)), color=WHITE_, line_length=0.2,
                     flash_radius=0.1, num_lines=10, run_time=0.35)

    def run(self, sc, t_end, rt1, rt2):
        sc.play(self.t.animate.set_value(0.0), rate_func=linear, run_time=rt1)
        sc.play(self.contato())
        self.t.set_value(1e-5)
        sc.play(self.t.animate.set_value(t_end), rate_func=linear, run_time=rt2)

    def solta(self):
        for m in (self.b1, self.b2, self.arrows):
            m.clear_updaters()


def estado_final(v1, v2, junto, escala=0.42, w1=1.1, w2=0.85, ka=0.55, kx=0.9, t=1.5):
    """Miniatura estática do estado depois do contato no exemplo-base (sem updaters)."""
    x1 = -w1 / 2 + v1 * t * kx
    x2 = w2 / 2 + v2 * t * kx
    b1 = Corpo("1", C1F, C1, w1, size=40).at(x1, 0)
    b2 = Corpo("2", C2F, C2, w2, size=40).at(x2, 0)
    trilho = Line(P3(min(x1, -2.0) - 1.0, 0), P3(max(x2, 2.0) + 1.0, 0), color=STEEL, stroke_width=3)
    g = VGroup(trilho, b1, b2)
    if junto:
        xm = (x1 + x2) / 2
        g.add(arrow(P3(xm, w1 + 0.3), P3(xm + v1 * ka, w1 + 0.3), width=6, tip=0.22))
    else:
        for x, w, v in ((x1, w1, v1), (x2, w2, v2)):
            if abs(v) > 0.05:
                g.add(arrow(P3(x, w + 0.3), P3(x + v * ka, w + 0.3), width=6, tip=0.22))
            else:
                g.add(MathTex("0", font_size=40, color=GREY).move_to(P3(x, w + 0.45)))
    return g.scale(escala)


class Colisoes1DYT013(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.add(self.wm)
        marcas = []
        for nome in ("c01_tres_finais", "c02_momento", "c03_energia", "c04_completamente_inelastica",
                     "c05_energia_cinetica", "c06_elastica_relativa", "c07_velocidades_gerais", "c08_casos_limite",
                     "c09_pendulo_setup", "c10_pendulo_impacto", "c11_pendulo_subida", "c12_metodo_e_ponte_2d"):
            if SECOES and nome[:3] not in SECOES:
                continue
            t0 = self.renderer.time
            getattr(self, nome)()
            marcas.append((nome, t0, self.renderer.time))
        for nome, a, b in marcas:
            print(f"[tempo] {nome}: {a:7.1f} s -> {b:7.1f} s ({b - a:5.1f} s)")

    # ── auditoria de sobreposições (desenvolvimento: AUDITORIA=1) ───────────────────────────────────────────
    def wait(self, *a, **kw):
        if AUDITORIA:
            self._auditar()
        return super().wait(*a, **kw)

    def _auditar(self):
        self.update_mobjects(0)            # estados de updaters atualizados antes de medir
        itens, linhas = [], []

        def op(m):
            """Opacidade real: a dos glifos (o MathTex por partes tem o contêiner com opacidade 0)."""
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
                if op(m) > 0.4:          # grade de fundo (opacidade 0.35) não conta
                    linhas.append(m)
                return
            if isinstance(m, Rectangle) and m.get_stroke_width() == 0 and m.get_fill_opacity() > 0.5:
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
                if x0 < -7.75 or x1 > 7.75 or y0 < -4.4 or y1 > 4.4:
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
        # texto atravessado por linhas (trilho, fios, contornos, divisórias, grades): amostra pontos da linha
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
    def clear(self, *keep, rt=0.7):
        keep = {self.wm, *keep}
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)
        for m in mobs:
            m.clear_updaters()
        self.remove(*mobs)

    def cap(self, s, y=-3.55, color=DIM, size=T_LAB):
        """Legenda curta da operação/ideia em curso (faixa inferior)."""
        return txt(s, size, color=color).move_to(P3(0, y))

    def troca(self, old, new, rt=0.5):
        if old is None:
            self.play(FadeIn(new), run_time=rt)
        else:
            self.play(FadeOut(old), FadeIn(new), run_time=rt)
        return new

    def swap(self, old, new, rt=1.1, **kw):
        self.play(TransformMatchingTex(old, new, **kw), run_time=rt)
        return new

    def remap(self, old, new, pairs, rt=1.2, extra=(), sem_fade=()):
        """Transformação explícita por partes: pairs = [(índices antigos, índices novos)]; o resto entra/sai em fade."""
        anims, uo, un = [], set(), set()
        for o, n in pairs:
            o = o if isinstance(o, (list, tuple)) else [o]
            n = n if isinstance(n, (list, tuple)) else [n]
            uo.update(o)
            un.update(n)
            anims.append(ReplacementTransform(VGroup(*[old[i].copy() for i in o]), VGroup(*[new[j] for j in n])))
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
        """Remove os mobjects e qualquer pedaço deles solto no topo da cena (TransformFromCopy etc.)."""
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

    def base_col(self, v1, v2, junto=None, **kw):
        m1, m2, u1, u2 = BASE
        args = dict(w1=1.1, w2=0.85, xc=0.3, ty=-1.6, kx=0.9, ka=0.55, t0=-1.5)
        args.update(kw)
        return Col(m1, m2, u1, u2, v1, v2, junto=junto, **args)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C01 — O mesmo começo, três finais (sem notação: só corpos, setas e a pergunta)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c01_tres_finais(self):
        slots = (-4.75, 0.0, 4.75)
        titulos = ("REBATEM", "SE SEPARAM", "FICAM JUNTOS")
        mesmo = txt("Mesmas massas, mesmas velocidades iniciais.", T_MAIN).move_to(P3(0, 3.25))
        leg = None
        for k, (nome, v1, v2) in enumerate(FINAIS):
            c = self.base_col(v1, v2, junto="" if nome == "ficam juntos" else None, n1="1", n2="2",
                              pre=(None, None), post=(None, None))
            if k == 0:
                self.play(FadeIn(c.group()), run_time=1.0)
                leg = self.troca(leg, self.cap("antes do impacto", y=-2.6))
                self.play(FadeIn(mesmo), run_time=0.7)
                self.wait(1.8)
            else:
                self.play(FadeIn(c.group()), run_time=0.6)
                leg = self.troca(leg, self.cap("antes do impacto", y=-2.6), rt=0.3)
                self.wait(0.6)
            c.run(self, 1.5, 1.3, 1.5)
            leg = self.troca(leg, self.cap("depois", y=-2.6), rt=0.3)
            t = txt(titulos[k], 40).move_to(P3(0.3, 0.55))
            self.play(FadeIn(t, shift=0.1 * UP), run_time=0.5)
            self.wait(1.2)
            mini = VGroup(estado_final(v1, v2, nome == "ficam juntos", escala=0.36), txt(titulos[k], T_LAB))
            mini[1].next_to(mini[0], DOWN, buff=0.18)
            mini.move_to(P3(slots[k], 1.85))
            c.solta()
            self.play(FadeOut(c.group()), ReplacementTransform(t, mini[1]), FadeIn(mini[0]), run_time=0.8)
        # um único estado inicial como referência
        ref = self.base_col(0, 0, n1="1", n2="2", pre=(None, None), post=(None, None))
        self.play(FadeIn(ref.group()), run_time=0.6)
        leg = self.troca(leg, self.cap("o mesmo início para os três", y=-2.6), rt=0.4)
        self.wait(1.4)
        dif = txt("O que muda é a interação durante o contato.", T_MAIN, color=GREY).move_to(P3(0, 0.4))
        self.play(FadeOut(mesmo), FadeIn(dif), run_time=0.7)
        self.wait(1.8)
        q = txt("O que falta saber sobre o contato?", 44, color=CYAN).move_to(P3(0, 0.4))
        self.play(FadeOut(dif), FadeIn(q, scale=0.96), run_time=0.8)
        self.wait(2.2)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C02 — Por que o momento se conserva? (notação, sinal, soma assinada, sistema, impulso, modelo ideal)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c02_momento(self):
        c = self.base_col(-2 / 3, 10 / 3, ty=-2.95, xc=0.6)      # desfecho "rebatem" do exemplo-base
        self.play(FadeIn(c.group()), run_time=0.8)
        # A — notação e sinal
        leg = VGroup(M("m", r"\ \text{massa}", size=M_LAB), M("u", r"\ \text{velocidade antes}", size=M_LAB),
                     M("v", r"\ \text{velocidade depois}", size=M_LAB),
                     M(r"1,\,2", r"\ \text{identificam os corpos}", size=M_LAB)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        leg.to_corner(UL, buff=0.45)
        self.play(LaggedStart(*[FadeIn(r) for r in leg], lag_ratio=0.3), run_time=1.6)
        self.wait(1.2)
        self.play(Indicate(c.track[1:], color=WHITE_, scale_factor=1.15), run_time=0.9)
        sinal = txt("para a esquerda: velocidade negativa", T_LAB, color=GREY).move_to(P3(2.4, -0.25))
        val = M("u_2", "=", r"-2\ \text{m/s}", size=M_LAB).next_to(sinal, UP, buff=0.15)
        self.play(FadeIn(sinal), FadeIn(val), Indicate(c.L["u_2"], color=WHITE_), run_time=0.9)
        self.wait(1.6)
        self.play(FadeOut(sinal), FadeOut(val), run_time=0.4)

        # p = mv e soma assinada numa reta com zero central
        pmv = M("p", "=", "m", "v", size=M_MID).move_to(P3(3.6, 2.7))
        self.play(FadeIn(pmv), run_time=0.6)
        nota = txt("mesma velocidade, mais massa: mais momento", T_SMALL, color=DIM).next_to(pmv, DOWN, buff=0.2)
        self.play(FadeIn(nota), run_time=0.5)
        self.wait(1.2)
        K, X0, YL = 0.62, -1.6, -0.15
        reta = VGroup(Line(P3(X0 - 3.0 * K, YL), P3(X0 + 6.2 * K, YL), color=STEEL, stroke_width=2.5))
        for v in range(-2, 7, 2):
            reta.add(Line(P3(X0 + v * K, YL - 0.08), P3(X0 + v * K, YL + 0.08), color=STEEL, stroke_width=2.5))
            reta.add(MathTex(f"{v:+d}" if v else "0", font_size=28, color=DIM).move_to(P3(X0 + v * K, YL - 0.32)))
        un = txt("momento (kg·m/s)", T_SMALL, color=DIM).next_to(reta[0], LEFT, buff=0.25)
        self.play(FadeOut(nota), Create(reta), FadeIn(un), run_time=0.9)
        a1 = arrow(P3(X0, YL + 1.0), P3(X0 + 4 * K, YL + 1.0), color=C1, width=7, tip=0.24)
        l1 = M("p_1", "=", "m_1u_1", "=", r"+4", size=M_LAB).next_to(a1, UP, buff=0.08)
        a2 = arrow(P3(X0, YL + 0.5), P3(X0 - 2 * K, YL + 0.5), color=C2, width=7, tip=0.24)
        l2 = M("p_2", "=", "m_2u_2", "=", r"-2", size=M_LAB).next_to(a2, LEFT, buff=0.15)
        self.play(Indicate(c.L["u_1"], color=WHITE_), GrowArrow(a1), FadeIn(l1), run_time=0.9)
        self.play(Indicate(c.L["u_2"], color=WHITE_), GrowArrow(a2), FadeIn(l2), run_time=0.9)
        self.wait(1.0)
        cp = self.cap("somar com sinal: p₂ começa onde p₁ termina")
        self.play(FadeIn(cp), run_time=0.4)
        self.play(a2.animate.shift(P3(4 * K, 0.5)), l2.animate.move_to(P3(X0 + 3 * K, YL + 1.95)), run_time=1.3)
        aP = arrow(P3(X0, YL + 0.45), P3(X0 + 2 * K, YL + 0.45), color=WHITE_, width=9, tip=0.26)
        gP = DashedLine(P3(X0 + 2 * K, YL + 1.0), P3(X0 + 2 * K, YL + 0.45), color=DIM, stroke_width=2)
        lP = M("P", "=", "p_1", "+", "p_2", "=", r"+2\ \text{kg}\cdot\text{m/s}", size=M_LAB)
        lP.next_to(P3(X0 + 6.4 * K, YL + 0.45), RIGHT, buff=0.3)
        self.play(Create(gP), GrowArrow(aP), FadeIn(lP), run_time=1.0)
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in (reta, un, a1, a2, l1, l2, aP, gP, lP, cp, leg, pmv)], run_time=0.6)

        # B — sistema e contato com força consistente (intervalo do contato ampliado)
        sist = contorno(VGroup(c.b1, c.b2, c.arrows), buff=0.25)
        ls = txt("sistema: corpo 1 + corpo 2", T_LAB, color=GREY).next_to(sist, UP, buff=0.12)
        self.play(Create(sist), FadeIn(ls), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(sist), FadeOut(ls), run_time=0.4)
        self.play(c.t.animate.set_value(0.0), rate_func=linear, run_time=1.4)
        s = ValueTracker(0.0)
        J = 4 - (-4 / 3)                       # momento trocado: Δp₂ = −Δp₁ = 16/3 kg·m/s
        K2, X2, YB = 0.48, -3.4, 1.15

        def bars():
            q = (1 - np.cos(PI * s.get_value())) / 2      # ∫ sen(πs) ds normalizada: mesma lei do gráfico
            p1, p2 = 4 - J * q, -2 + J * q
            return VGroup(arrow(P3(X2, YB + 0.7), P3(X2 + p1 * K2, YB + 0.7), color=C1, width=7, tip=0.22),
                          arrow(P3(X2, YB + 0.15), P3(X2 + p2 * K2, YB + 0.15), color=C2, width=7, tip=0.22),
                          arrow(P3(X2, YB - 0.45), P3(X2 + (p1 + p2) * K2, YB - 0.45), color=WHITE_, width=9,
                                tip=0.24))

        zero = VGroup(DashedLine(P3(X2, YB + 1.05), P3(X2, YB - 0.75), color=DIM, stroke_width=2),
                      MathTex("0", font_size=28, color=DIM).move_to(P3(X2, YB - 0.95)))
        labs = VGroup(M("p_1", size=M_LAB).move_to(P3(X2 - 2.6, YB + 0.7)),
                      M("p_2", size=M_LAB).move_to(P3(X2 - 2.6, YB + 0.15)),
                      M("P", size=M_LAB).move_to(P3(X2 - 2.6, YB - 0.45)))
        bv = always_redraw(bars)
        # força × tempo (área = impulso trocado); a mesma lei alimenta as setas de momento
        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1.1, 1], x_length=3.6, y_length=1.9, tips=False,
                  axis_config={"color": STEEL, "stroke_width": 2}).move_to(P3(4.6, 1.25))
        axl = VGroup(txt("t", T_SMALL, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.1),
                     txt("força de contato", T_SMALL, color=DIM).next_to(ax.y_axis, UP, buff=0.1))
        curva = ax.plot(lambda x: np.sin(PI * x), x_range=[0, 1], color=WHITE_, stroke_width=3)
        area = always_redraw(lambda: ax.get_area(curva, x_range=[0, max(s.get_value(), 1e-3)], color=CYAN, opacity=0.35))
        la = txt("área = impulso trocado", T_SMALL, color=CYAN).next_to(ax, DOWN, buff=0.2)

        def forcas():
            f = np.sin(PI * s.get_value())
            if f < 0.03:
                return VGroup()
            y = c.ty + 0.45
            return VGroup(arrow(P3(c.xc - 0.03, y), P3(c.xc - 0.03 - 1.5 * f, y), width=7, tip=0.24),
                          arrow(P3(c.xc + 0.03, y), P3(c.xc + 0.03 + 1.5 * f, y), width=7, tip=0.24)).set_z_index(12)

        fz = always_redraw(forcas)
        c.ao.set_value(0)
        self.play(FadeIn(bv), FadeIn(zero), FadeIn(labs), Create(ax), FadeIn(axl), Create(curva), run_time=0.9)
        self.add(area, fz)
        amp = self.cap("intervalo do contato ampliado no tempo")
        self.play(FadeIn(amp), run_time=0.4)
        self.play(s.animate.set_value(1.0), rate_func=linear, run_time=4.0)
        self.play(FadeIn(la), run_time=0.4)
        tr = M(r"\text{trocam momento entre si: }", r"\Delta p_1", "=", r"-\Delta p_2", size=M_LAB).move_to(P3(-1.6, -0.15))
        self.play(FadeIn(tr), run_time=0.6)
        self.wait(1.6)
        nt = txt("na soma, as variações internas se cancelam: P não muda", T_LAB, color=GREY).move_to(P3(-1.6, -0.75))
        self.play(FadeIn(nt), run_time=0.5)
        self.wait(1.8)
        self.remove(fz)
        c.t.set_value(1e-5)
        self.play(c.t.animate.set_value(0.9), c.ao.animate.set_value(1), rate_func=linear, run_time=1.2)
        area.clear_updaters()
        bv.clear_updaters()
        self.play(*[FadeOut(m) for m in (bv, zero, labs, ax, axl, curva, area, la, tr, nt, amp)], run_time=0.6)

        # C — impulso externo e modelo ideal
        e1 = M(r"\Delta P_x", "=", r"J_{\mathrm{ext},x}", size=M_MAIN).move_to(P3(-2.6, 2.4))
        e1b = M(r"J_{\mathrm{ext},x}=\int_{t_i}^{t_f}F_{\mathrm{ext},x}\,dt", size=M_REF).move_to(P3(3.6, 2.4))
        self.play(FadeIn(e1), run_time=0.7)
        self.play(FadeIn(e1b), run_time=0.7)
        n1 = txt("forças internas: impulsos opostos, somam zero no sistema", T_LAB, color=GREY).move_to(P3(0, 1.45))
        n2 = txt("externas horizontais (atrito, ar): impulso desprezível neste contato", T_LAB, color=GREY) \
            .move_to(P3(0, 0.95))
        self.play(FadeIn(n1), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(n2), run_time=0.6)
        self.wait(1.6)
        e2 = M(r"J_{\mathrm{ext},x}\approx 0", r"\ \Rightarrow\ ", r"P_{x,f}\approx P_{x,i}", size=M_MAIN).move_to(P3(0, 0.0))
        self.play(FadeIn(e2), run_time=0.8)
        self.wait(1.4)
        ideal = txt("No modelo ideal: impulso externo horizontal = zero.", T_MAIN, color=CYAN) \
            .move_to(P3(0, -0.85))
        self.play(FadeIn(ideal), run_time=0.8)
        self.wait(1.6)
        e3 = M("P_{x,i}", "=", "P_{x,f}", size=M_MAIN).move_to(P3(0, 0.0))
        self.play(ReplacementTransform(e2, e3), run_time=0.8)
        self.wait(1.0)
        e4 = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_MAIN).move_to(P3(0, 0.0))
        self.play(FadeOut(n1), FadeOut(n2), FadeOut(ideal), FadeOut(e1), FadeOut(e1b), run_time=0.5)
        self.play(TransformFromCopy(c.L["u_1"], e4[0]), TransformFromCopy(c.L["u_2"], e4[2]),
                  TransformFromCopy(c.L["v_1"], e4[4]), TransformFromCopy(c.L["v_2"], e4[6]),
                  FadeOut(e3), FadeIn(e4[1]), FadeIn(e4[3]), FadeIn(e4[5]), run_time=1.3)
        self.settle(e4)
        self.wait(1.0)
        kn = txt("conhecidos", T_LAB, color=DIM).next_to(e4[:3], UP, buff=0.3)
        vv = VGroup(e4.get_part_by_tex("v_1"), e4.get_part_by_tex("v_2"))
        bxs = VGroup(*[box(m, buff=0.07) for m in vv])
        inc = txt("incógnitas", T_LAB, color=CYAN).next_to(e4[4:], UP, buff=0.3)
        self.play(FadeIn(kn), run_time=0.5)
        self.play(Create(bxs), FadeIn(inc), run_time=0.7)
        um = txt("uma equação, duas velocidades desconhecidas", T_MAIN).move_to(P3(0, -0.95))
        self.play(FadeIn(um), run_time=0.7)
        self.wait(1.6)
        dica = txt("Escolha sistema, eixo e intervalo antes de escolher a conservação.", T_LAB, color=CYAN) \
            .move_to(P3(0, 2.6))
        self.play(FadeIn(dica), run_time=0.6)
        self.wait(2.2)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C03 — O que a energia nos diz sobre o contato? (nomes formais entram aqui)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c03_energia(self):
        k1 = M("K", "=", r"\tfrac{1}{2}", "m", "v^2", size=M_MAIN).move_to(P3(-3.2, 2.2))
        k2 = M(r"K_{\mathrm{total}}", "=", "K_1", "+", "K_2", size=M_MAIN).move_to(P3(3.4, 2.2))
        self.play(FadeIn(k1), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(k2), run_time=0.8)
        n1 = txt("K é escalar e nunca negativa: o quadrado remove o sinal de v", T_LAB, color=GREY).move_to(P3(0, 1.1))
        n2 = txt("K mede o movimento dos corpos; aquecimento e deformação são energia interna", T_LAB, color=GREY) \
            .move_to(P3(0, 0.55))
        self.play(FadeIn(n1), run_time=0.6)
        self.wait(1.2)
        self.play(FadeIn(n2), run_time=0.6)
        self.wait(1.8)
        self.clear()

        # Mesmos três desfechos, mesma escala de energia (K_i = 6 J; P = +2 kg·m/s nos três)
        KE = 0.72                                   # tela por joule
        XB = 0.9
        topo = VGroup(txt("antes", T_LAB, color=DIM), barra(XB, 2.75, 6 * KE, CYAN),
                      M("K_i", "=", r"6\ \text{J}", size=M_LAB))
        topo[0].move_to(P3(-1.0, 2.75))
        topo[2].next_to(topo[1], RIGHT, buff=0.25)
        pn = M(r"P", "=", r"+2\ \text{kg}\cdot\text{m/s}", r"\text{ nos três}", size=M_LAB, color=GREY).move_to(P3(-4.6, 2.75))
        self.play(FadeIn(topo), FadeIn(pn), run_time=0.8)
        self.wait(0.8)
        ys = (1.45, 0.0, -1.55)
        nomes = (VGroup(txt("ELÁSTICA", 34, color=CYAN)), VGroup(txt("INELÁSTICA", 34, color=CYAN)),
                 VGroup(txt("COMPLETAMENTE", 30, color=CYAN), txt("INELÁSTICA", 30, color=CYAN)).arrange(DOWN, buff=0.08))
        KF = (6.0, 2.0, 2 / 3)
        conds = (M("K_f", "=", "K_i", size=M_LAB), M("K_f", "<", "K_i", size=M_LAB), M("v_1", "=", "v_2", size=M_LAB))
        notas = (txt("o que o contato guarda volta ao movimento", T_SMALL, color=DIM),
                 txt("magenta: virou energia interna", T_SMALL, color=MAG),
                 M("K_f", r"\text{ não é zero em geral}", size=32, color=DIM))
        for k, (nm, v1, v2) in enumerate(FINAIS):
            y = ys[k]
            mini = estado_final(v1, v2, nm == "ficam juntos", escala=0.3).move_to(P3(-5.2, y))
            nomes[k].move_to(P3(-1.75, y))
            bk = barra(XB, y, 6 * KE, CYAN)
            self.play(FadeIn(mini), FadeIn(bk), run_time=0.6)
            self.play(FadeIn(nomes[k], shift=0.1 * UP), run_time=0.5)
            if KF[k] < 6:
                mg = barra(XB + KF[k] * KE, y, (6 - KF[k]) * KE, MAG)
                self.play(Transform(bk, barra(XB, y, KF[k] * KE, CYAN)), FadeIn(mg), run_time=1.1)
            conds[k].move_to(P3(XB + 6 * KE + 0.95, y))
            if notas[k].width > 5.6:
                notas[k].scale_to_fit_width(5.6)
            notas[k].move_to(P3(XB + notas[k].width / 2, y - 0.37))
            self.play(FadeIn(conds[k]), FadeIn(notas[k]), run_time=0.5)
            self.wait(1.4)
        # completamente inelástica é caso particular das inelásticas
        br = Brace(VGroup(nomes[1], nomes[2]), LEFT, buff=0.15, color=GREY)
        lb = txt("inelásticas", T_SMALL, color=GREY).next_to(br, LEFT, buff=0.1)
        part = txt("caso particular", T_SMALL, color=DIM).next_to(nomes[2], DOWN, buff=0.1)
        self.play(FadeIn(br), FadeIn(lb), FadeIn(part), run_time=0.8)
        self.wait(2.0)
        self.clear()

        l1 = VGroup(txt("Elástica", T_MAIN, color=CYAN), M(r"\rightarrow", size=M_MID), M("K_f", "=", "K_i", size=M_MID)) \
            .arrange(RIGHT, buff=0.35)
        l2 = VGroup(txt("Ficam juntos", T_MAIN, color=CYAN), M(r"\rightarrow", size=M_MID),
                    M("v_1", "=", "v_2", size=M_MID)).arrange(RIGHT, buff=0.35)
        l3 = VGroup(txt("Só “inelástica”", T_MAIN, color=CYAN), M(r"\rightarrow", size=M_MID),
                    M("K_f", "<", "K_i", size=M_MID)).arrange(RIGHT, buff=0.35)
        VGroup(l1, l2, l3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(P3(-1.0, 1.0))
        xs = max(l.get_right()[0] for l in (l1, l2, l3)) + 0.6
        s1 = txt("2ª equação", T_LAB, color=GREY)
        s2 = txt("2ª equação", T_LAB, color=GREY)
        s3 = txt("restringe, mas não fecha", T_LAB, color=MAG)
        for l, s_ in ((l1, s1), (l2, s2), (l3, s3)):
            s_.move_to(P3(xs + s_.width / 2, l.get_center()[1]))
        for l, s_ in ((l1, s1), (l2, s2), (l3, s3)):
            self.play(FadeIn(l), run_time=0.6)
            self.play(FadeIn(s_), run_time=0.4)
            self.wait(1.0)
        fim = txt("momento + condição adicional suficiente", 44, color=CYAN).move_to(P3(0, -2.0))
        self.play(FadeIn(fim, scale=0.96), Create(box(fim, buff=0.22)), run_time=0.9)
        self.wait(2.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C04 — Quando os corpos ficam juntos
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c04_completamente_inelastica(self):
        m1, m2, u1, u2 = 2.0, 1.0, 2.0, -1.0
        vf = (m1 * u1 + m2 * u2) / (m1 + m2)
        c = Col(m1, m2, u1, u2, vf, vf, w1=1.1, w2=0.85, xc=-0.3, ty=-2.8, kx=0.9, ka=0.6, t0=-1.6, junto="v_f")
        self.play(FadeIn(c.group()), run_time=0.8)
        self.wait(0.6)
        c.run(self, 1.4, 1.5, 1.4)
        cond = M(r"\text{ficam juntos}", r"\ \Rightarrow\ ", "v_1", "=", "v_2", "=", "v_f", size=M_MID).move_to(P3(0, 2.75))
        self.play(FadeIn(cond, shift=0.1 * UP), run_time=0.8)
        self.wait(1.0)
        pi = M("P_i", "=", "m_1u_1", "+", "m_2u_2", size=M_MID).move_to(P3(-3.6, 1.55))
        pf = M("P_f", "=", "m_1v_f", "+", "m_2v_f", size=M_MID).move_to(P3(3.6, 1.55))
        self.play(FadeIn(pi), run_time=0.7)
        self.play(FadeIn(pf), run_time=0.7)
        self.wait(0.8)
        fc = self.troca(None, self.cap("fator comum"))
        pf2 = M("P_f", "=", "(m_1+m_2)", "v_f", size=M_MID).move_to(pf)
        self.remap(pf, pf2, [(0, 0), (1, 1), ([2, 3, 4], [2, 3])], rt=1.1)
        pf = pf2
        self.wait(0.8)
        eq = M("m_1u_1", "+", "m_2u_2", "=", "(m_1+m_2)", "v_f", size=M_MAIN).move_to(P3(0, 0.35))
        fc = self.troca(fc, self.cap("momento antes = momento depois"))
        self.play(TransformFromCopy(pi[2:], eq[:3]), FadeIn(eq[3]), TransformFromCopy(pf[2:], eq[4:]), run_time=1.2)
        self.settle(eq)
        self.wait(1.0)
        fc = self.troca(fc, self.cap("dividir os dois lados por m₁ + m₂ > 0"))
        res = M("v_f", "=", r"\frac{m_1u_1+m_2u_2}{m_1+m_2}", size=M_MAIN).move_to(P3(0, 0.35))
        self.play(FadeOut(pi), FadeOut(pf), run_time=0.4)
        self.remap(eq, res, [([0, 1, 2, 4], 2), (5, 0), (3, 1)], rt=1.3)
        bx = box(res)
        self.play(Create(bx), run_time=0.5)
        self.wait(1.6)

        # média ponderada numa reta de velocidades (não é o trilho)
        c.solta()
        self.play(FadeOut(c.group()), FadeOut(cond), FadeOut(fc), VGroup(res, bx).animate.move_to(P3(0, 2.45)),
                  run_time=0.9)
        wf = M("v_f", "=", r"\frac{m_1}{m_1+m_2}", "u_1", "+", r"\frac{m_2}{m_1+m_2}", "u_2", size=M_MAIN) \
            .move_to(P3(0, 2.45))
        self.play(FadeOut(bx), ReplacementTransform(res, wf), run_time=1.0)
        pesos = txt("pesos positivos que somam 1", T_LAB, color=GREY).next_to(wf, DOWN, buff=0.2)
        self.play(FadeIn(pesos), run_time=0.5)
        self.wait(1.2)
        KV, X0, Y = 2.0, -1.0, -1.2

        def X(v):
            return X0 + KV * v

        reta = VGroup(arrow(P3(X(-1.7), Y), P3(X(2.6), Y), color=STEEL, width=3, tip=0.16))
        for v in (-1, 0, 1, 2):
            reta.add(Line(P3(X(v), Y - 0.09), P3(X(v), Y + 0.09), color=STEEL, stroke_width=3))
            reta.add(MathTex(str(v), font_size=30, color=DIM).move_to(P3(X(v), Y - 0.38)))
        rl = txt("eixo de velocidades, v (m/s) — não é o trilho", T_SMALL, color=DIM).next_to(reta, DOWN, buff=0.55)
        mu1 = VGroup(Dot(P3(X(u1), Y), radius=0.08, color=C1), M("u_1", size=M_LAB).move_to(P3(X(u1), Y + 0.45)))
        mu2 = VGroup(Dot(P3(X(u2), Y), radius=0.08, color=C2), M("u_2", size=M_LAB).move_to(P3(X(u2), Y + 0.45)))
        self.play(Create(reta), FadeIn(rl), FadeIn(mu1), FadeIn(mu2), run_time=1.0)
        r = ValueTracker(m1 / (m1 + m2))

        def xv():
            return X(r.get_value() * u1 + (1 - r.get_value()) * u2)

        vmk = always_redraw(lambda: VGroup(Dot(P3(xv(), Y), radius=0.11, color=CYAN).set_z_index(6),
                                           M("v_f", size=M_LAB, color=CYAN).move_to(P3(xv(), Y + 0.95))))
        rt = M("m_1", ":", "m_2", "=", "2", ":", "1", size=M_MID).move_to(P3(-4.8, -0.2))
        self.play(FadeIn(vmk), FadeIn(rt), run_time=0.7)
        self.wait(1.2)
        for a, b in ((1, 1), (1, 4), (4, 1)):
            nr = M("m_1", ":", "m_2", "=", str(a), ":", str(b), size=M_MID).move_to(rt)
            self.play(r.animate.set_value(a / (a + b)), TransformMatchingTex(rt, nr), run_time=1.3)
            rt = nr
            if (a, b) == (1, 4):
                ng = M("v_f", "<", "0", r"\text{: o par sai para a esquerda}", size=34, color=GREY).move_to(P3(X(-0.4), Y + 1.55))
                self.play(FadeIn(ng), run_time=0.4)
                self.wait(1.2)
                self.play(FadeOut(ng), run_time=0.3)
            else:
                self.wait(1.0)
        fim = M("v_f", r"\text{ fica entre }", "u_2", r"\text{ e }", "u_1",
                r"\text{, mais perto da velocidade do corpo mais pesado}", size=36, color=CYAN).move_to(P3(0, -3.55))
        self.play(FadeIn(fim), run_time=0.6)
        self.wait(2.0)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C05 — Momento conservado não implica K conservada
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c05_energia_cinetica(self):
        intro = M(r"\text{agora: }", "m_1", "=", "m_2", "=", "m", r",\quad ", "u_2", "=", "0", size=M_MID).move_to(P3(0, 3.0))
        self.play(FadeIn(intro), run_time=0.7)
        c = Col(1, 1, 2.0, 0.0, 1.0, 1.0, w1=0.95, w2=0.95, xc=-3.4, ty=0.55, kx=0.8, ka=0.7, t0=-1.6,
                n1="m", n2="m", pre=("u", False), junto="v_f", trilho=(-7.3, 0.9))
        self.play(FadeIn(c.group()), run_time=0.8)
        c.run(self, 1.3, 1.4, 1.3)
        XE = 3.7
        e = M("m", "u", "=", "2m", "v_f", size=M_MID).move_to(P3(XE, 1.85))
        self.play(FadeIn(e), run_time=0.7)
        self.wait(0.8)
        e2 = M("v_f", "=", r"\frac{u}{2}", size=M_MID).move_to(P3(XE, 1.85))
        self.remap(e, e2, [(4, 0), (2, 1), ([1, 3], 2)], rt=1.1)
        self.wait(0.6)
        q = txt("Metade da velocidade significa metade da energia?", T_MAIN, color=GREY).move_to(P3(0, -0.45))
        self.play(FadeIn(q), run_time=0.7)
        self.wait(1.8)
        self.play(FadeOut(q), FadeOut(intro), run_time=0.4)
        k1 = M("K_i", "=", r"\tfrac{1}{2}", "m", "u^2", size=M_MID).move_to(P3(XE, 0.7))
        self.play(FadeIn(k1), run_time=0.7)
        k2 = M("K_f", "=", r"\tfrac{1}{2}", "(2m)", r"\left(\tfrac{u}{2}\right)^2", size=M_MID).move_to(P3(XE, -0.55))
        self.play(FadeIn(k2), run_time=0.8)
        b1 = box(k2[3], color=GREY, buff=0.06)
        lb1 = txt("massa total dobra", T_SMALL, color=GREY).next_to(b1, DOWN, buff=0.12)
        self.play(Create(b1), FadeIn(lb1), run_time=0.6)
        self.wait(1.0)
        k3 = M("K_f", "=", r"\tfrac{1}{2}", "(2m)", r"\frac{u^2}{4}", size=M_MID).move_to(k2)
        lb2 = M(r"\left(\tfrac{u}{2}\right)^2=\tfrac{u^2}{4}", size=M_LAB, color=CYAN).move_to(P3(XE, -2.0))
        lb3 = txt("velocidade ao quadrado: divide por 4", T_SMALL, color=CYAN).next_to(lb2, DOWN, buff=0.12)
        self.play(FadeOut(b1), FadeOut(lb1), FadeIn(lb2), FadeIn(lb3), run_time=0.6)
        self.remap(k2, k3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], rt=1.0)
        self.wait(1.2)
        k4 = M("K_f", "=", r"\tfrac{1}{4}", "m", "u^2", size=M_MID).move_to(k2)
        self.play(FadeOut(lb2), FadeOut(lb3), run_time=0.3)
        self.remap(k3, k4, [(0, 0), (1, 1), ([2, 3, 4], [2, 3, 4])], rt=1.0)
        self.wait(0.8)
        k5 = M("K_f", "=", r"\tfrac{1}{2}", "K_i", size=M_MID).move_to(k2)
        self.remap(k4, k5, [(0, 0), (1, 1), ([2, 3, 4], [2, 3])], rt=1.0)
        self.play(Create(box(k5)), run_time=0.4)

        # barras pela mesma conta: m = 1 kg, u = 2 m/s → K_i = 2 J, K_f = 1 J; P_i = P_f = 2 kg·m/s
        KE, XB, YB = 2.2, -6.6, -1.35
        num = M(r"m=1\ \text{kg},\ u=2\ \text{m/s}", size=34, color=DIM).move_to(P3(-4.4, -0.35))
        bi = barra(XB, YB, 2 * KE, CYAN)
        li = M("K_i", "=", r"2\ \text{J}", size=M_LAB).next_to(bi, RIGHT, buff=0.2)
        self.play(FadeIn(num), FadeIn(bi), FadeIn(li), run_time=0.7)
        bf = barra(XB, YB - 0.75, 2 * KE, CYAN)
        self.play(FadeIn(bf), run_time=0.4)
        mg = barra(XB + KE, YB - 0.75, KE, MAG)
        lf = M("K_f", "=", r"1\ \text{J}", size=M_LAB).next_to(barra(XB, YB - 0.75, 2 * KE, CYAN), RIGHT, buff=0.2)
        self.play(Transform(bf, barra(XB, YB - 0.75, KE, CYAN)), FadeIn(mg), FadeIn(lf), run_time=1.1)
        lm = txt("1 J → energia interna (deformação, aquecimento, vibração)", T_SMALL, color=MAG) \
            .next_to(VGroup(bf, mg), DOWN, buff=0.15, aligned_edge=LEFT)
        pp = M("P_i", "=", "P_f", "=", r"2\ \text{kg}\cdot\text{m/s}", size=M_LAB, color=GREY).move_to(P3(-4.4, -3.35))
        self.play(FadeIn(lm), FadeIn(pp), run_time=0.6)
        self.wait(2.2)
        self.clear(c.b1, c.b2, c.track, c.arrows)
        f1 = txt("Momento: soma com sinal (linear) — se mantém.", T_MAIN).move_to(P3(0, -1.0))
        f2 = txt("Energia cinética: soma de quadrados — pode mudar.", T_MAIN, color=CYAN).move_to(P3(0, -1.75))
        self.play(FadeIn(f1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(f2), run_time=0.7)
        self.wait(2.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C06 — Derivação elástica: de duas conservações à velocidade relativa (núcleo)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c06_elastica_relativa(self):
        m1, m2, u1, u2 = 1.0, 2.0, 3.0, 0.0
        v1, v2 = -1.0, 2.0
        c = Col(m1, m2, u1, u2, v1, v2, w1=0.85, w2=1.1, xc=0.0, ty=-2.2, kx=0.9, ka=0.5, t0=-1.6,
                pre=("u_1", "u_2=0"))
        hd = txt("Agora, a colisão elástica.", T_MAIN, color=GREY).move_to(P3(0, 2.9))
        self.play(FadeIn(hd), FadeIn(c.group()), run_time=0.9)
        c.run(self, 1.3, 1.4, 1.3)
        w1_ = txt("impulso externo horizontal ≈ 0  →  momento", T_LAB, color=GREY).move_to(P3(0, 1.8))
        w2_ = txt("colisão elástica  →  energia cinética conservada", T_LAB, color=GREY).move_to(P3(0, 1.3))
        self.play(FadeIn(w1_), run_time=0.5)
        self.play(FadeIn(w2_), run_time=0.5)
        self.wait(1.6)
        c.solta()
        self.play(FadeOut(c.group()), FadeOut(hd), FadeOut(w1_), FadeOut(w2_), run_time=0.7)

        # A — montar e reorganizar
        P = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_MAIN).move_to(P3(0, 1.4))
        E = M(r"\tfrac{1}{2}m_1u_1^2", "+", r"\tfrac{1}{2}m_2u_2^2", "=", r"\tfrac{1}{2}m_1v_1^2", "+",
              r"\tfrac{1}{2}m_2v_2^2", size=M_MAIN).move_to(P3(0, -0.5))
        self.play(Write(P), run_time=1.2)
        self.play(Write(E), run_time=1.4)
        self.wait(1.6)
        self.play(E.animate.set_opacity(0.25), run_time=0.4)
        op = self.troca(None, self.cap("termos do corpo 1 à esquerda, do corpo 2 à direita"))
        P2 = M("m_1u_1", "-", "m_1v_1", "=", "m_2v_2", "-", "m_2u_2", size=M_MAIN).move_to(P)
        P = self.swap(P, P2, rt=1.3)
        self.wait(1.0)
        op = self.troca(op, self.cap("fator comum em cada lado"))
        P3_ = M("m_1", "(u_1-v_1)", "=", "m_2", "(v_2-u_2)", size=M_MAIN).move_to(P)
        self.remap(P, P3_, [([0, 2], [0, 1]), (3, 2), ([4, 6], [3, 4])], rt=1.2)
        P = P3_
        n1 = M("(1)", size=M_LAB, color=DIM)
        self.wait(1.0)
        self.play(P.animate.scale(0.78).move_to(P3(-0.3, 2.85)), run_time=0.8)
        n1.next_to(P, RIGHT, buff=0.45)
        self.play(FadeIn(n1), E.animate.set_opacity(1).move_to(P3(0, 0.9)), run_time=0.8)
        # energia: multiplicar AMBOS os lados por 2
        op = self.troca(op, self.cap("multiplicar ambos os lados por 2"))
        xl = M(r"\times 2", size=M_LAB, color=CYAN).next_to(E[:3], DOWN, buff=0.25)
        xr = M(r"\times 2", size=M_LAB, color=CYAN).next_to(E[4:], DOWN, buff=0.25)
        self.play(FadeIn(xl), FadeIn(xr), run_time=0.6)
        self.wait(0.6)
        E2 = M("m_1u_1^2", "+", "m_2u_2^2", "=", "m_1v_1^2", "+", "m_2v_2^2", size=M_MAIN).move_to(E)
        self.remap(E, E2, [(i, i) for i in range(7)], rt=1.1, extra=[FadeOut(xl), FadeOut(xr)])
        E = E2
        self.wait(0.6)
        op = self.troca(op, self.cap("de novo: corpo 1 à esquerda, corpo 2 à direita"))
        E3 = M("m_1u_1^2", "-", "m_1v_1^2", "=", "m_2v_2^2", "-", "m_2u_2^2", size=M_MAIN).move_to(E)
        E = self.swap(E, E3, rt=1.2)
        self.wait(0.6)
        op = self.troca(op, self.cap("fator comum"))
        E4 = M("m_1", r"(u_1^2-v_1^2)", "=", "m_2", r"(v_2^2-u_2^2)", size=M_MAIN).move_to(E)
        self.remap(E, E4, [([0, 2], [0, 1]), (3, 2), ([4, 6], [3, 4])], rt=1.2)
        E = E4
        self.wait(0.8)

        # B — diferença de quadrados, um lado de cada vez
        op = self.troca(op, self.cap("diferença de quadrados"))
        regra = M("a^2-b^2", "=", "(a-b)(a+b)", size=M_MID, color=CYAN).move_to(P3(0, -0.6))
        self.play(FadeIn(regra), run_time=0.6)
        self.wait(1.0)
        bL = box(E[1], buff=0.07)
        self.play(Create(bL), run_time=0.4)
        E5 = M("m_1", "(u_1-v_1)(u_1+v_1)", "=", "m_2", r"(v_2^2-u_2^2)", size=M_MAIN).move_to(E)
        self.remap(E, E5, [(0, 0), (2, 2), (3, 3), (4, 4)], rt=1.2, extra=[FadeOut(bL)])
        E = E5
        self.wait(0.6)
        bR = box(E[4], buff=0.07)
        self.play(Create(bR), run_time=0.4)
        E6 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "=", "m_2", "(v_2-u_2)", "(v_2+u_2)", size=M_MAIN).move_to(E)
        self.remap(E, E6, [(0, 0), (1, [1, 2]), (2, 3), (3, 4)], rt=1.2, extra=[FadeOut(bR)])
        E = E6
        n2 = M("(2)", size=M_LAB, color=DIM).next_to(E, RIGHT, buff=0.4)
        self.play(FadeOut(regra), FadeIn(n2), run_time=0.5)
        self.wait(1.2)

        # C — substituir (1) em (2) sem dividir
        op = self.troca(op, self.cap("não dividimos: usamos (1) dentro de (2)"))
        bA = box(VGroup(E[4], E[5]), buff=0.07)
        bB = box(VGroup(P[3], P[4]), buff=0.07)
        self.play(Create(bA), Create(bB), run_time=0.7)
        self.wait(0.8)
        bC = box(VGroup(P[0], P[1]), buff=0.07)
        self.play(ReplacementTransform(bB, bC), run_time=0.7)
        E7 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "=", "m_1", "(u_1-v_1)", "(v_2+u_2)", size=M_MAIN).move_to(E)
        self.play(FadeOut(bA), FadeOut(E[4]), FadeOut(E[5]), FadeOut(n2),
                  ReplacementTransform(VGroup(*E[:4], E[6]).copy(), VGroup(*E7[:4], E7[6])),
                  TransformFromCopy(P[0], E7[4]), TransformFromCopy(P[1], E7[5]), run_time=1.3)
        self.drop(E)
        self.settle(E7)
        E = E7
        self.play(FadeOut(bC), run_time=0.3)
        self.wait(1.0)
        op = self.troca(op, self.cap("subtrair o lado direito dos dois lados"))
        E8 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "-", "m_1", "(u_1-v_1)", "(v_2+u_2)", "=", "0", size=M_MAIN,
               w=14.2).move_to(E)
        self.remap(E, E8, [(0, 0), (1, 1), (2, 2), (3, 7), (4, 4), (5, 5), (6, 6)], rt=1.2)
        E = E8
        self.wait(1.0)
        op = self.troca(op, self.cap("fator comum m₁(u₁ − v₁)"))
        E9 = M("m_1", "(u_1-v_1)", r"\big[", "(u_1+v_1)", "-", "(v_2+u_2)", r"\big]", "=", "0", size=M_MAIN).move_to(E)
        self.remap(E, E9, [([0, 4], 0), ([1, 5], 1), (2, 3), (3, 4), (6, 5), (7, 7), (8, 8)], rt=1.4)
        E = E9
        self.wait(0.8)
        op = self.troca(op, self.cap("produto nulo, com m₁ > 0: um dos outros fatores é zero"))
        self.wait(2.0)

        # Ramos
        self.play(FadeOut(P), FadeOut(n1), FadeOut(op), E.animate.scale(0.85).move_to(P3(0, 2.75)), run_time=0.8)
        XL, XR = -3.8, 3.5
        sep = DashedLine(P3(-0.2, 2.0), P3(-0.2, -3.2), color=DIM, stroke_width=2)
        a1 = arrow(E[1].get_bottom() + DOWN * 0.1, P3(XL, 1.9), color=DIM, width=3, tip=0.14)
        a2 = arrow(E[2:7].get_bottom() + DOWN * 0.1, P3(XR, 1.9), color=DIM, width=3, tip=0.14)
        self.play(Create(sep), GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        L1 = M("u_1-v_1", "=", "0", size=M_MID).move_to(P3(XL, 1.35))
        self.play(FadeIn(L1), run_time=0.5)
        L2 = M("u_1", "=", "v_1", size=M_MID).move_to(P3(XL, 0.45))
        L3 = M(r"\text{por (1): }", "u_2", "=", "v_2", size=M_MID).move_to(P3(XL, -0.4))
        self.play(FadeIn(L2), run_time=0.5)
        self.play(FadeIn(L3), run_time=0.6)
        tri = VGroup(txt("ramo trivial", T_LAB, color=GREY),
                     txt("mesmas velocidades: nenhuma", T_SMALL, color=DIM),
                     txt("transferência líquida de momento", T_SMALL, color=DIM)).arrange(DOWN, buff=0.1)
        tri.move_to(P3(XL, -1.55))
        self.play(FadeIn(tri), run_time=0.7)
        nao = VGroup(txt("não é o encontro com interação", T_SMALL, color=DIM),
                     txt("que estamos resolvendo", T_SMALL, color=DIM)).arrange(DOWN, buff=0.06).move_to(P3(XL, -2.7))
        self.play(FadeIn(nao), run_time=0.5)
        self.wait(1.4)
        R1 = M("(u_1+v_1)", "-", "(v_2+u_2)", "=", "0", size=M_MID).move_to(P3(XR, 1.35))
        self.play(FadeIn(R1), run_time=0.6)
        R2 = M("u_1", "+", "v_1", "=", "v_2", "+", "u_2", size=M_MID).move_to(P3(XR, 0.45))
        self.play(FadeIn(R2, shift=0.15 * DOWN), run_time=0.7)
        R3 = M("u_1", "-", "u_2", "=", "v_2", "-", "v_1", size=M_MID).move_to(P3(XR, -0.45))
        self.play(FadeIn(R3, shift=0.15 * DOWN), run_time=0.7)
        R4 = M("u_1", "-", "u_2", "=", "-", "(v_1-v_2)", size=M_MAIN).move_to(P3(XR, -1.55))
        self.play(FadeIn(R4, shift=0.15 * DOWN), run_time=0.8)
        br = box(R4, buff=0.16)
        ef = txt("ramo da colisão efetiva", T_LAB, color=CYAN).next_to(br, DOWN, buff=0.2)
        self.play(Create(br), FadeIn(ef), VGroup(L1, L2, L3, tri, nao, a1).animate.set_opacity(0.35), run_time=0.8)
        self.wait(2.2)

        # D — interpretação: distância entre centros d = x2 − x1
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.wm, R3)], run_time=0.6)
        self.play(R3.animate.move_to(P3(0, 2.85)), run_time=0.7)
        c = Col(m1, m2, u1, u2, v1, v2, w1=0.85, w2=1.1, xc=-2.3, ty=-2.2, kx=0.75, ka=0.45, t0=-1.5,
                pre=("u_1", False), post=("v_1", "v_2"), eixo=False)

        def d_atual():
            return c.x2() - c.x1()

        def regua():
            x1, x2 = c.x1(), c.x2()
            y = c.ty - 0.45
            g = VGroup(DoubleArrow(P3(x1, y), P3(x2, y), buff=0, color=CYAN, stroke_width=4, tip_length=0.16,
                                   max_tip_length_to_length_ratio=0.3),
                       Line(P3(x1, c.ty + 0.4), P3(x1, y - 0.12), color=DIM, stroke_width=1.5),
                       Line(P3(x2, c.ty + 0.4), P3(x2, y - 0.12), color=DIM, stroke_width=1.5))
            g.add(MathTex("d", font_size=M_LAB, color=CYAN).move_to(P3((x1 + x2) / 2, y - 0.35)))
            return g

        rg = always_redraw(regua)
        dd = M("d", "=", "x_2", "-", "x_1", size=M_LAB, color=CYAN).move_to(P3(-4.6, 1.9))
        nd = txt("distância entre os centros", T_SMALL, color=DIM).next_to(dd, DOWN, buff=0.12)
        self.play(FadeIn(c.group()), FadeIn(rg), FadeIn(dd), FadeIn(nd), run_time=0.9)
        # gráfico d × t calculado do mesmo estado
        dc = (c.w1 + c.w2) / 2
        tmin, tmax = -1.5, 1.5
        dmax = dc + (u1 - u2) * 1.5 * c.kx
        ax = Axes(x_range=[tmin, tmax, 0.5], y_range=[0, dmax * 1.05, 1], x_length=4.0, y_length=2.5, tips=False,
                  axis_config={"color": STEEL, "stroke_width": 2}).move_to(P3(4.9, -0.75))
        axl = VGroup(txt("t", T_SMALL, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.1),
                     txt("d", T_SMALL, color=CYAN).next_to(ax.y_axis, UP, buff=0.08))

        def dlei(t):
            return dc + ((u2 - u1) if t < 0 else (v2 - v1)) * t * c.kx

        traco = always_redraw(lambda: ax.plot(dlei, x_range=[tmin, max(c.t.get_value(), tmin + 1e-3)],
                                              color=CYAN, stroke_width=4))
        cur = always_redraw(lambda: Dot(ax.c2p(c.t.get_value(), d_atual()), radius=0.08, color=WHITE_).set_z_index(6))
        self.play(Create(ax), FadeIn(axl), run_time=0.7)
        self.add(traco, cur)
        self.play(c.t.animate.set_value(0.0), rate_func=linear, run_time=2.2)
        ta = M(r"\text{antes: } d \text{ diminui } (u_1-u_2) \text{ por segundo}", size=36, color=GREY).move_to(P3(-1.0, 1.15))
        self.play(FadeIn(ta), run_time=0.5)
        self.wait(1.0)
        self.play(c.contato())
        c.t.set_value(1e-5)
        self.play(c.t.animate.set_value(1.5), rate_func=linear, run_time=2.2)
        tb = M(r"\text{depois: } d \text{ aumenta } (v_2-v_1) \text{ por segundo}", size=36, color=GREY).move_to(P3(-1.0, 0.6))
        self.play(FadeIn(tb), run_time=0.5)
        self.wait(1.2)
        f1 = M(r"\text{aproximação }(u_1-u_2)", "=", r"\text{afastamento }(v_2-v_1)", size=M_REF).move_to(P3(0, 2.85))
        self.play(FadeOut(R3), FadeIn(f1), run_time=0.8)
        self.wait(1.6)
        f2 = M("u_1", "-", "u_2", "=", "-", "(v_1-v_2)", size=M_MAIN).move_to(P3(0, 2.85))
        self.play(FadeOut(f1), FadeIn(f2), run_time=0.8)
        self.play(Create(box(f2, buff=0.15)), run_time=0.5)
        pay = txt("O que se inverte é a velocidade relativa —", T_MAIN, color=CYAN).move_to(P3(-0.9, 1.95))
        pay2 = txt("cada corpo não precisa inverter a própria velocidade.", T_LAB, color=GREY).move_to(P3(-0.9, 1.5))
        self.play(FadeOut(ta), FadeOut(tb), FadeOut(dd), FadeOut(nd), FadeIn(pay), run_time=0.7)
        self.play(FadeIn(pay2), run_time=0.5)
        self.wait(2.6)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C07 — As fórmulas gerais nascem da resolução do sistema
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c07_velocidades_gerais(self):
        A = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_REF).move_to(P3(-3.6, 3.0))
        B = M("u_1", "-", "u_2", "=", "v_2", "-", "v_1", size=M_REF).move_to(P3(3.9, 3.0))
        la = txt("momento", T_SMALL, color=DIM).next_to(A, DOWN, buff=0.1)
        lb = txt("relação da colisão elástica", T_SMALL, color=DIM).next_to(B, DOWN, buff=0.1)
        self.play(FadeIn(A), FadeIn(la), FadeIn(B), FadeIn(lb), run_time=0.9)
        self.wait(1.0)
        op = self.troca(None, self.cap("isolar v₂"))
        s1 = M("v_2", "=", "u_1-u_2", "+", "v_1", size=M_MID).move_to(P3(3.9, 1.75))
        self.play(TransformFromCopy(B, s1), run_time=1.1)
        self.settle(s1)
        self.wait(1.0)
        s2 = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_MAIN).move_to(P3(0, 0.3))
        self.play(TransformFromCopy(A, s2), run_time=1.0)
        self.settle(s2)
        op = self.troca(op, self.cap("substituir o bloco inteiro no lugar de v₂"))
        bv = box(s2[6], buff=0.07)
        self.play(Create(bv), Indicate(s1, color=CYAN), run_time=0.8)
        s3 = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2", "(u_1-u_2+v_1)", size=M_MAIN).move_to(s2)
        self.play(FadeOut(bv), run_time=0.2)
        self.remap(s2, s3, [(i, i) for i in range(6)], rt=0.9, extra=[TransformFromCopy(s1[2:], s3[7])], sem_fade=(7,))
        self.settle(s3)
        self.wait(1.2)
        op = self.troca(op, self.cap("distributiva: m₂ multiplica cada termo"))
        s4 = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2u_1", "-", "m_2u_2", "+", "m_2v_1", size=M_MAIN,
               w=14.2).move_to(s2)
        self.remap(s3, s4, [(i, i) for i in range(6)] + [([6, 7], [6, 7, 8, 9, 10])], rt=1.3)
        sn = box(VGroup(s4[7], s4[8]), color=MAG, buff=0.06)
        sl = txt("o sinal de −m₂u₂ vem de −u₂", T_SMALL, color=MAG).next_to(sn, DOWN, buff=0.15)
        self.play(Create(sn), FadeIn(sl), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(sn), FadeOut(sl), run_time=0.3)
        op = self.troca(op, self.cap("termos com v₁ à direita; o resto à esquerda"))
        s5 = M("m_1u_1", "-", "m_2u_1", "+", "m_2u_2", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_1", size=M_MAIN,
               w=14.2).move_to(s2)
        self.swap(s4, s5, rt=1.6)
        self.wait(1.4)
        op = self.troca(op, self.cap("fator comum"))
        s6 = M("(m_1-m_2)", "u_1", "+", "2m_2u_2", "=", "(m_1+m_2)", "v_1", size=M_MAIN).move_to(s2)
        self.remap(s5, s6, [([0, 1, 2], [0, 1]), ([3, 4, 5, 6], [2, 3]), (7, 4), ([8, 9, 10], [5, 6])], rt=1.3)
        self.wait(1.2)
        op = self.troca(op, self.cap("dividir ambos os lados por m₁ + m₂"))
        s7 = M("v_1", "=", r"\frac{m_1-m_2}{m_1+m_2}", "u_1", "+", r"\frac{2m_2}{m_1+m_2}", "u_2", size=M_MAIN).move_to(s2)
        self.remap(s6, s7, [(6, 0), (4, 1), ([0, 5], 2), (1, 3), (2, 4), (3, [5, 6])], rt=1.4)
        b7 = box(s7)
        self.play(Create(b7), run_time=0.5)
        self.wait(1.6)

        # v2 a partir de v2 = u1 − u2 + v1
        self.play(VGroup(s7, b7).animate.scale(0.72).move_to(P3(-3.4, 1.5)), FadeOut(A), FadeOut(la), run_time=0.8)
        op = self.troca(op, self.cap("substituir v₁ em v₂ = u₁ − u₂ + v₁"))
        t1 = M("v_2", "=", r"\left[1+\frac{m_1-m_2}{m_1+m_2}\right]", "u_1", "+",
               r"\left[-1+\frac{2m_2}{m_1+m_2}\right]", "u_2", size=M_MID).move_to(P3(0, -0.6))
        self.play(FadeIn(t1, shift=0.15 * DOWN), run_time=1.0)
        self.wait(1.4)
        c1 = M(r"1+\frac{m_1-m_2}{m_1+m_2}=\frac{2m_1}{m_1+m_2}", size=M_LAB, color=GREY).move_to(P3(-3.6, -2.15))
        c2 = M(r"-1+\frac{2m_2}{m_1+m_2}=\frac{m_2-m_1}{m_1+m_2}", size=M_LAB, color=GREY).move_to(P3(3.6, -2.15))
        op = self.troca(op, self.cap("mesmo denominador em cada colchete"))
        self.play(FadeIn(c1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(c2), run_time=0.7)
        self.wait(1.2)
        t2 = M("v_2", "=", r"\frac{2m_1}{m_1+m_2}", "u_1", "+", r"\frac{m_2-m_1}{m_1+m_2}", "u_2", size=M_MAIN).move_to(t1)
        self.remap(t1, t2, [(i, i) for i in range(7)], rt=1.2)
        b8 = box(t2)
        self.play(Create(b8), FadeOut(c1), FadeOut(c2), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(op), FadeOut(B), FadeOut(lb), FadeOut(s1), run_time=0.4)
        res = VGroup(VGroup(s7, b7), VGroup(t2, b8))
        self.play(res.animate.arrange(DOWN, buff=0.25).scale_to_fit_height(2.1).move_to(P3(0, 1.9)), run_time=0.9)
        n1 = txt("Valem para colisão elástica em 1D — não são fórmulas universais.", T_LAB, color=GREY).move_to(P3(0, 0.25))
        n2 = txt("Coeficientes sem unidade: o resultado sai em m/s.", T_LAB, color=GREY).move_to(P3(0, -0.3))
        self.play(FadeIn(n1), run_time=0.6)
        self.play(FadeIn(n2), run_time=0.6)
        self.wait(1.2)
        met = txt("Método: montar as equações + condição física.", T_MAIN, color=CYAN).move_to(P3(0, -1.4))
        self.play(FadeIn(met), run_time=0.7)
        self.wait(2.2)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C08 — Três casos-limite como testes de plausibilidade (massas finitas; ≈ na tela)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c08_casos_limite(self):
        hd = txt("Em vez de decorar, testar.", T_MAIN, color=GREY).move_to(P3(0, 3.1))
        lu = M(r"\text{com }", "u_2", "=", "0", r"\text{:}", size=M_LAB, color=DIM)
        g1 = M("v_1", "=", r"\frac{m_1-m_2}{m_1+m_2}", "u_1", size=M_REF)
        g2 = M("v_2", "=", r"\frac{2m_1}{m_1+m_2}", "u_1", size=M_REF)
        VGroup(lu, g1, g2).arrange(RIGHT, buff=0.9).move_to(P3(0, 2.25))
        self.play(FadeIn(hd), run_time=0.5)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(lu), run_time=0.9)
        self.wait(1.0)
        u1 = 2.4
        casos = (
            (1.0, 1.0, 0.95, 0.95, "massas iguais", "previsão: o primeiro para?",
             (M("v_1", "=", "0", size=M_MID), M("v_2", "=", "u_1", size=M_MID)), None),
            (1.0, 30.0, 0.75, 1.25, "leve contra pesado", "previsão: o leve volta?",
             (M("v_1", "=", r"-\tfrac{29}{31}u_1", r"\approx", "-u_1", size=M_MID),
              M("v_2", "=", r"\tfrac{2}{31}u_1", r"\approx", "0", size=M_MID)), r"m_2 = 30\,m_1"),
            (30.0, 1.0, 1.25, 0.75, "pesado contra leve", "previsão: o leve dispara?",
             (M("v_1", "=", r"\tfrac{29}{31}u_1", r"\approx", "u_1", size=M_MID),
              M("v_2", "=", r"\tfrac{60}{31}u_1", r"\approx", "2u_1", size=M_MID)), r"m_1 = 30\,m_2"),
        )
        for m1, m2, w1, w2, nome, prev, res, nota in casos:
            v1 = (m1 - m2) / (m1 + m2) * u1
            v2 = 2 * m1 / (m1 + m2) * u1
            c = Col(m1, m2, u1, 0.0, v1, v2, w1=w1, w2=w2, xc=-1.4, ty=-2.6, kx=0.9, ka=0.45, t0=-1.5,
                    pre=("u_1", "u_2=0"), post=("v_1" if abs(v1) > 0.05 else "v_1=0", "v_2"))
            tn = VGroup(txt(nome, T_MAIN, color=CYAN), txt(prev, T_LAB, color=GREY)).arrange(DOWN, buff=0.12,
                                                                                          aligned_edge=LEFT)
            if nota:
                tn.add(M(nota, size=M_LAB, color=GREY))
                tn[-1].next_to(tn[1], DOWN, buff=0.12, aligned_edge=LEFT)
            tn.move_to(P3(-4.2, 0.3))
            self.play(FadeIn(c.group()), FadeIn(tn), run_time=0.8)
            self.wait(1.2)
            rs = VGroup(*res).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(P3(3.4, 0.3))
            self.play(FadeIn(rs, shift=0.1 * DOWN), run_time=0.8)
            self.wait(1.4)
            x2a = c.x2()
            c.run(self, 1.5, 1.3, 1.6)
            if m2 > m1:
                # o pesado ainda se move: marca do deslocamento na mesma escala (sem fator oculto)
                x2b = c.x2()
                y = c.ty - 0.3
                mk = VGroup(Line(P3(x2a, y - 0.12), P3(x2a, y + 0.12), color=C2, stroke_width=3),
                            Line(P3(x2b, y - 0.12), P3(x2b, y + 0.12), color=C2, stroke_width=3),
                            Line(P3(x2a, y), P3(x2b, y), color=C2, stroke_width=3))
                lm = M(r"\text{o pesado ainda se move: }", r"\Delta x_2", r"> 0", size=34, color=C2).next_to(mk, DOWN, buff=0.12)
                self.play(Create(mk), FadeIn(lm), run_time=0.6)
            if m1 > m2:
                lm = txt("o leve recebe energia do pesado: nada é criado", T_MAIN, color=GREY).move_to(hd)
                self.play(FadeOut(hd), FadeIn(lm), run_time=0.5)
            brs = box(rs, buff=0.18)
            ok = txt("confere", T_LAB, color=CYAN).next_to(brs, LEFT, buff=0.25)
            self.play(Create(brs), FadeIn(ok), run_time=0.6)
            self.wait(1.8)
            c.solta()
            self.clear(hd, g1, g2, lu, rt=0.5)
        self.play(*[FadeOut(m) for m in (g1, g2, lu, hd) if m in self.mobjects], run_time=0.4)
        s = txt("Casos-limite: testes de plausibilidade", 44, color=CYAN).move_to(P3(0, 0.5))
        d = txt("Antes de aceitar uma fórmula: sinais, massas iguais, massa muito grande.", T_LAB, color=GREY) \
            .move_to(P3(0, -0.4))
        self.play(FadeIn(s, scale=0.96), run_time=0.8)
        self.play(FadeIn(d), run_time=0.6)
        self.wait(2.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C09–C11 — Pêndulo balístico (suspensão bifilar: o bloco translada, sem girar)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def _pendulo(self):
        """Constrói o aparato no estado A. Cada seção do pêndulo chama isto (trecho isolado funciona)."""
        PX, PY = -3.0, 2.2
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
        teto = VGroup(Line(P3(PX - 1.3, PY), P3(PX + 1.3, PY), color=STEEL, stroke_width=4),
                      *[Line(P3(x - 0.1, PY + 0.2), P3(x + 0.1, PY), color=STEEL, stroke_width=2)
                        for x in np.linspace(PX - 1.2, PX + 1.2, 10)])
        piv = VGroup(Dot(P3(PX - A, PY), radius=0.06, color=GREY), Dot(P3(PX + A, PY), radius=0.06, color=GREY))

        def desenho():
            cc = centro()
            blk = Corpo("M", C2F, C2, BW, size=40, alt=BH).at(cc[0], cc[1] - BH / 2)
            top = cc[1] + BH / 2
            fios = VGroup(Line(P3(PX - A, PY), P3(cc[0] - A, top), color=GREY, stroke_width=2.5),
                          Line(P3(PX + A, PY), P3(cc[0] + A, top), color=GREY, stroke_width=2.5))
            g = VGroup(fios, blk)
            if self.dentro:
                g.add(RoundedRectangle(corner_radius=0.04, width=0.32, height=0.13, stroke_width=0, fill_color=C1,
                                       fill_opacity=1).move_to(cc + LEFT * (BW / 2 - 0.22)).set_z_index(5))
            return g

        def bala():
            if self.dentro:
                return VGroup()
            y = centro()[1]
            b = RoundedRectangle(corner_radius=0.04, width=0.32, height=0.13, stroke_width=0, fill_color=C1,
                                 fill_opacity=1).move_to(P3(self.bx.get_value(), y))
            return VGroup(b, MathTex("m", font_size=34, color=WHITE_).next_to(b, DOWN, buff=0.12))

        self.estat = VGroup(teto, piv)
        self.pend = always_redraw(desenho)
        self.bal = always_redraw(bala)
        self.xin = PX - BW / 2 + 0.22         # x da bala alojada no bloco (estado B)

    def _th(self, tau):
        return float(np.interp(tau, SUB_T, SUB_TH))

    def _om(self, tau):
        return float(np.interp(tau, SUB_T, SUB_W))

    def _marca_h(self):
        yB = self.PY - PL * ESC - self.BH / 2
        yC = self.centro()[1]
        xr = self.centro()[0] + self.BW / 2 + 0.35
        l0 = DashedLine(P3(self.PX - 1.2, yB), P3(xr, yB), color=DIM, stroke_width=2)
        l1 = DashedLine(P3(self.PX - 1.2, yC), P3(xr, yC), color=DIM, stroke_width=2)
        br = Brace(Line(P3(xr, yB), P3(xr, yC)), RIGHT, buff=0.06, color=WHITE_)
        lh = MathTex("h", font_size=40, color=WHITE_).next_to(br, RIGHT, buff=0.1)
        return VGroup(l0, l1, br, lh)

    def _seta_V(self):
        cc = self.centro()
        b = arrow(P3(cc[0] + 1.0, cc[1]), P3(cc[0] + 1.9, cc[1]), width=5, tip=0.18)
        return VGroup(b, MathTex("V", font_size=40, color=CYAN).next_to(b, UP, buff=0.06))

    def _seta_u(self):
        cc = self.centro()
        a = arrow(P3(-6.3, cc[1] + 0.35), P3(-5.4, cc[1] + 0.35), width=5, tip=0.18)
        return VGroup(a, MathTex("u", font_size=40).next_to(a, UP, buff=0.06))

    def _subir(self, rt, *extra):
        """Subida B → C em tempo físico integrado, exibida desacelerada uniformemente."""
        tau = ValueTracker(0.0)
        self.tau = tau
        self.th.add_updater(lambda m: m.set_value(self._th(tau.get_value())))
        self.play(tau.animate.set_value(SUB_T[-1]), *extra, rate_func=linear, run_time=rt)
        self.th.clear_updaters()
        self.th.set_value(SUB_TH[-1])

    def c09_pendulo_setup(self):
        self._pendulo()
        q = VGroup(txt("Dá para descobrir a velocidade do projétil", T_MAIN),
                   txt("medindo a altura da subida?", T_MAIN)).arrange(DOWN, buff=0.1).move_to(P3(0.6, 3.05))
        self.play(FadeIn(q), FadeIn(self.estat), FadeIn(self.pend), FadeIn(self.bal), run_time=1.0)
        dados = VGroup(M(r"\text{dados: }", "m", r",\ ", "M", r",\ ", "h", size=M_LAB),
                       M(r"\text{incógnita: }", "u", size=M_LAB, color=CYAN)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        dados.move_to(P3(4.3, 1.5))
        self.play(FadeIn(dados), run_time=0.7)
        defs = VGroup(M("u", r"\text{: projétil, antes do impacto}", size=36, color=GREY),
                      M("V", r"\text{: conjunto, logo depois}", size=36, color=GREY)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        defs.next_to(dados, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(defs), run_time=0.7)
        self.wait(1.0)
        cc = self.centro()
        lu = self._seta_u()
        tA = txt("A: antes", T_LAB, color=C1).move_to(P3(-5.9, -2.35))
        self.play(FadeIn(lu), FadeIn(tA), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(lu), self.bx.animate.set_value(self.xin), rate_func=linear, run_time=1.0)
        self.dentro = True
        lV = self._seta_V()
        tB = txt("B: logo depois", T_LAB, color=CYAN).move_to(P3(cc[0], -2.35))
        self.play(FadeIn(lV), FadeIn(tB), run_time=0.6)
        self.wait(1.2)
        ghostB = self.pend.copy().clear_updaters().set_opacity(0.22)
        self.add(ghostB)
        self._subir(2.4, FadeOut(lV))
        hm = self._marca_h()
        tC = txt("C: altura máxima", T_LAB, color=UG).move_to(P3(0.6, -2.35))
        self.play(FadeIn(hm), FadeIn(tC), run_time=0.7)
        self.wait(1.2)
        e1 = txt("A → B: impacto", T_MAIN, color=C1).move_to(P3(3.3, -1.2))
        e2 = txt("B → C: subida", T_MAIN, color=UG).move_to(P3(3.3, -1.85))
        self.play(FadeIn(e1), run_time=0.5)
        self.play(FadeIn(e2), run_time=0.5)
        dica = txt("Pergunte o que acontece em cada intervalo.", T_LAB, color=CYAN).move_to(P3(0, -3.3))
        self.play(FadeIn(dica), run_time=0.5)
        self.wait(2.0)
        self.clear()

    def c10_pendulo_impacto(self):
        self._pendulo()                      # estado A
        self.play(FadeIn(self.estat), FadeIn(self.pend), FadeIn(self.bal), run_time=0.7)
        tt = txt("A → B: impacto", T_MAIN, color=C1).move_to(P3(-3.0, 3.3))
        self.play(FadeIn(tt), run_time=0.4)
        cc = self.centro()
        sist = contorno(Rectangle(width=7.0, height=2.0).move_to(P3(-3.5, cc[1] - 0.05)), buff=0.05)
        ls = txt("sistema: projétil + bloco", T_SMALL, color=GREY).next_to(sist, DOWN, buff=0.1, aligned_edge=LEFT)
        self.play(Create(sist), FadeIn(ls), run_time=0.8)
        eixo = VGroup(arrow(P3(-3.2, cc[1] - 1.75), P3(-0.4, cc[1] - 1.75), color=DIM, width=3, tip=0.16),
                      MathTex("+x", font_size=34, color=DIM).move_to(P3(-0.05, cc[1] - 1.75)))
        peso = VGroup(arrow(cc, cc + DOWN * 0.9, color=GREY, width=3.5, tip=0.15),
                      txt("peso", T_SMALL, color=GREY).move_to(cc + DOWN * 0.7 + RIGHT * 0.5))
        tens = VGroup(arrow(cc + P3(-0.55, self.BH / 2), cc + P3(-0.55, self.BH / 2 + 0.75), color=GREY, width=3.5, tip=0.15),
                      arrow(cc + P3(0.55, self.BH / 2), cc + P3(0.55, self.BH / 2 + 0.75), color=GREY, width=3.5, tip=0.15),
                      txt("tensões (verticais)", T_SMALL, color=GREY).move_to(cc + P3(2.35, self.BH / 2 + 1.05)))
        self.play(FadeIn(eixo), FadeIn(peso), FadeIn(tens), run_time=0.8)
        nv = VGroup()
        im = txt("impacto breve: impulso externo horizontal desprezível → modelo ideal (= 0)", T_LAB) \
            .move_to(P3(0, -3.5))
        self.play(FadeIn(im), run_time=0.6)
        self.wait(1.4)
        XE = 4.1
        pa = M("P_{x,A}", "=", "m", "u", "+", r"M\cdot 0", size=M_MID).move_to(P3(XE, 1.9))
        lu = self._seta_u()
        self.play(FadeIn(lu), run_time=0.3)
        self.play(TransformFromCopy(lu[1], pa[3]), FadeIn(pa[:3]), FadeIn(pa[4:]), run_time=1.0)
        self.settle(pa)
        self.wait(0.8)
        self.play(FadeOut(lu), FadeOut(tens), self.bx.animate.set_value(self.xin), rate_func=linear, run_time=0.9)
        self.dentro = True
        lV = self._seta_V()
        self.play(FadeIn(lV), run_time=0.4)
        pb = M("P_{x,B}", "=", "m", "V", "+", "M", "V", size=M_MID).move_to(P3(XE, 0.85))
        self.play(FadeIn(pb), run_time=0.8)
        pb2 = M("P_{x,B}", "=", "(m+M)", "V", size=M_MID).move_to(pb)
        cv = txt("ficou preso: velocidade comum", T_SMALL, color=DIM).next_to(pb2, DOWN, buff=0.15)
        self.remap(pb, pb2, [(0, 0), (1, 1), ([2, 4, 5], 2), ([3, 6], 3)], rt=1.1)
        self.play(FadeIn(cv), run_time=0.4)
        self.wait(1.0)
        pa2 = M("P_{x,A}", "=", "m", "u", size=M_MID).move_to(pa)
        self.remap(pa, pa2, [(0, 0), (1, 1), (2, 2), (3, 3)], rt=0.8)
        eq = M("m", "u", "=", "(m+M)", "V", size=M_MAIN).move_to(P3(XE, -0.6))
        self.play(TransformFromCopy(pa2[2:], eq[:2]), FadeIn(eq[2]), TransformFromCopy(pb2[2:], eq[3:]), run_time=1.1)
        self.settle(eq)
        bq = box(eq)
        self.play(Create(bq), run_time=0.4)
        self.wait(1.2)
        # K cai no impacto: K_B/K_A = m/(m+M) = 0,02 (barras na mesma escala)
        L0, XB, YK = 4.4, 1.8, -2.3
        self.play(FadeOut(cv), FadeOut(nv), FadeOut(im), run_time=0.3)
        kA = barra(XB, YK, L0, CYAN, h=0.26)
        kB = barra(XB, YK - 0.5, L0 * PM / (PM + PMM), CYAN, h=0.26)
        lk = VGroup(M("K_A", size=36).next_to(kA, LEFT, buff=0.12), M("K_B", size=36).next_to(kB, LEFT, buff=0.12))
        rz = M(r"\frac{K_B}{K_A}=\frac{m}{m+M}=2\%", size=36, color=GREY).next_to(kB, RIGHT, buff=0.3)
        nr = txt("com m = 20 g e M = 980 g", T_SMALL, color=DIM).next_to(rz, DOWN, buff=0.08, aligned_edge=LEFT)
        self.play(FadeIn(kA), FadeIn(kB), FadeIn(lk), run_time=0.6)
        self.play(FadeIn(rz), FadeIn(nr), run_time=0.6)
        nk = txt("K não se conserva no impacto", T_SMALL, color=GREY).next_to(kA, UP, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(nk), run_time=0.4)
        self.wait(1.8)
        # memória do estado B: V e a equação do impacto
        self.play(*[FadeOut(m) for m in (kA, kB, lk, rz, nr, nk, sist, ls, eixo, peso, pa2, pb2, bq)], run_time=0.6)
        self.play(eq.animate.scale(0.7).move_to(P3(4.6, 2.75)), run_time=0.7)
        self.eq_imp = eq
        self.lV = lV
        self.play(Indicate(eq[4], color=CYAN), Indicate(lV[1], color=CYAN), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(tt), run_time=0.3)

    def c11_pendulo_subida(self):
        if not hasattr(self, "eq_imp"):        # trecho isolado: reconstrói o estado B
            self._pendulo()
            self.dentro = True
            self.lV = self._seta_V()
            self.eq_imp = M("m", "u", "=", "(m+M)", "V", size=M_MAIN).scale(0.7).move_to(P3(4.6, 2.75))
            self.add(self.estat, self.pend, self.bal, self.lV, self.eq_imp)
        tt = txt("B → C: subida", T_MAIN, color=UG).move_to(P3(-3.0, 3.3))
        hip = txt("sem ar, sem atrito nos suportes, fios ideais, bloco sem giro", T_SMALL, color=DIM).move_to(P3(-3.0, 2.9))
        self.play(FadeIn(tt), FadeIn(hip), run_time=0.6)
        tn = txt("tensão perpendicular ao movimento: trabalho nulo", T_SMALL, color=GREY).move_to(P3(-3.0, -2.75))
        nm = txt("o momento linear NÃO se conserva na subida", T_SMALL, color=GREY).move_to(P3(-3.0, -3.2))
        self.play(FadeIn(tn), FadeIn(nm), run_time=0.6)
        yB = self.centro()[1]
        ref = VGroup(DashedLine(P3(-6.4, yB), P3(self.centro()[0] - self.BW / 2 - 0.15, yB), color=UG, stroke_width=2),
                     M("U_g=0", size=34).move_to(P3(-5.6, yB + 0.3)))
        self.play(FadeIn(ref), run_time=0.5)
        # tabela B | C
        XT = 4.2
        hdr = VGroup(txt("B", T_MAIN, color=CYAN).move_to(P3(XT - 1.75, 1.75)), txt("C", T_MAIN, color=UG).move_to(P3(XT + 1.75, 1.75)))
        lin = Line(P3(XT, 2.0), P3(XT, -0.75), color=STEEL, stroke_width=2)
        rows = VGroup(
            M("v=V", size=M_LAB).move_to(P3(XT - 1.75, 1.15)), M("v=0", size=M_LAB).move_to(P3(XT + 1.75, 1.15)),
            M(r"K_B=\tfrac12(m+M)V^2", size=34).move_to(P3(XT - 1.75, 0.45)), M("K_C=0", size=M_LAB).move_to(P3(XT + 1.75, 0.45)),
            M("U_B=0", size=M_LAB).move_to(P3(XT - 1.75, -0.3)), M("U_C=(m+M)gh", size=34).move_to(P3(XT + 1.75, -0.3)))
        self.play(FadeOut(self.eq_imp), FadeIn(hdr), Create(lin), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=1.6)
        self.wait(1.4)
        # subida em tempo físico (integrado); K e U_g vêm do mesmo estado (θ, ω)
        KE = 2.6 / (0.5 * PV ** 2)          # tela por (J/kg)
        self.tau = ValueTracker(0.0)

        def barras():
            tv = self.tau.get_value()
            th, om = self._th(tv), self._om(tv)
            k = 0.5 * (PL * om) ** 2
            u = PG * PL * (1 - np.cos(th))
            return VGroup(barra(0.9, -1.75, k * KE, CYAN, h=0.28), barra(0.9, -2.3, u * KE, UG, h=0.28))

        bars = always_redraw(barras)
        lbars = VGroup(M("K", size=36, color=CYAN).move_to(P3(0.6, -1.75)), M("U_g", size=36).move_to(P3(0.55, -2.3)))
        sc = txt("mesma escala: K + U_g constante", T_SMALL, color=DIM).move_to(P3(5.0, -2.75))
        self.play(FadeIn(bars), FadeIn(lbars), FadeIn(sc), run_time=0.5)
        tau = self.tau
        self.th.add_updater(lambda m: m.set_value(self._th(tau.get_value())))
        self.play(FadeOut(self.lV), tau.animate.set_value(SUB_T[-1]), rate_func=linear, run_time=3.2)
        self.th.clear_updaters()
        self.th.set_value(SUB_TH[-1])
        bars.clear_updaters()
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in (hdr, lin, rows, bars, lbars, sc)], run_time=0.5)
        hm = self._marca_h()
        nh = VGroup(txt("h: elevação do conjunto", T_SMALL, color=DIM), txt("(não é o arco)", T_SMALL, color=DIM)) \
            .arrange(DOWN, buff=0.06).move_to(P3(-5.4, self.centro()[1] + 0.55))
        self.play(FadeIn(hm), FadeIn(nh), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(tn), FadeOut(nm), run_time=0.4)
        XE = 3.7
        e1 = M(r"\tfrac{1}{2}", "(m+M)", "V^2", "=", "(m+M)", "g", "h", size=M_MID).move_to(P3(XE, 1.8))
        lb = txt("energia mecânica: B = C", T_SMALL, color=DIM).next_to(e1, UP, buff=0.12)
        self.play(FadeIn(e1), FadeIn(lb), run_time=0.8)
        self.wait(1.0)
        op = self.troca(None, self.cap("cancelar (m + M) > 0 nos dois lados"))
        e2 = M(r"\tfrac{1}{2}", "V^2", "=", "g", "h", size=M_MID).move_to(e1)
        self.remap(e1, e2, [(0, 0), (2, 1), (3, 2), (5, 3), (6, 4)], rt=1.1)
        self.wait(0.6)
        op = self.troca(op, self.cap("multiplicar ambos os lados por 2"))
        e3 = M("V^2", "=", "2", "g", "h", size=M_MID).move_to(e1)
        self.remap(e2, e3, [(1, 0), (2, 1), (3, 3), (4, 4)], rt=1.0)
        self.wait(0.6)
        op = self.troca(op, self.cap("V é o módulo da velocidade (para a direita): raiz positiva"))
        e4 = M("V", "=", r"\sqrt{2gh}", size=M_MID).move_to(e1)
        self.remap(e3, e4, [(0, 0), (1, 1), ([2, 3, 4], 2)], rt=1.0)
        self.play(Create(box(e4)), run_time=0.4)
        self.wait(1.0)
        op = self.troca(op, self.cap("voltar ao impacto"))
        eqi = M("m", "u", "=", "(m+M)", "V", size=M_MID).move_to(P3(XE, 0.5))
        self.play(FadeIn(eqi), run_time=0.6)
        e5 = M("u", "=", r"\frac{m+M}{m}", "V", size=M_MID).move_to(eqi)
        self.remap(eqi, e5, [(1, 0), (2, 1), ([0, 3], 2), (4, 3)], rt=1.1)
        self.wait(0.6)
        e6 = M("u", "=", r"\frac{m+M}{m}", r"\sqrt{2gh}", size=M_MID).move_to(P3(XE, -0.9))
        self.play(TransformFromCopy(e5[:3], e6[:3]), TransformFromCopy(e4[2], e6[3]), run_time=1.1)
        self.settle(e6)
        self.play(Create(box(e6)), run_time=0.4)
        self.wait(1.0)
        cad = txt("h medida  →  V depois do impacto  →  u antes do impacto", T_LAB, color=CYAN).move_to(P3(0, -3.55))
        self.play(FadeOut(op), FadeIn(cad), run_time=0.6)
        self.wait(1.6)
        pl = VGroup(M(r"\sqrt{gh}\ \text{tem unidade de velocidade}", size=32, color=GREY),
                    M(r"h=0\ \Rightarrow\ u=0", size=32, color=GREY),
                    M(r"\text{projétil leve: } u \gg V", size=32, color=GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        pl.move_to(P3(XE, -2.3))
        self.play(FadeIn(pl), run_time=0.7)
        self.wait(2.0)
        self.clear()
        r1 = VGroup(txt("impacto", 40, color=C1), M(r"\rightarrow", size=M_MID), txt("momento horizontal", T_MAIN)) \
            .arrange(RIGHT, buff=0.4)
        r2 = VGroup(txt("subida", 40, color=UG), M(r"\rightarrow", size=M_MID), txt("energia mecânica", T_MAIN)) \
            .arrange(RIGHT, buff=0.4)
        VGroup(r1, r2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(P3(0, 0.9))
        self.play(FadeIn(r1), run_time=0.6)
        self.play(FadeIn(r2), run_time=0.6)
        pay = txt("Cada intervalo físico pode exigir uma lei diferente.", 42, color=CYAN).move_to(P3(0, -0.9))
        self.play(FadeIn(pay, shift=0.1 * UP), run_time=0.8)
        self.wait(2.6)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C12 — Método aplicado e ponte (teaser) para 2D
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c12_metodo_e_ponte_2d(self):
        hd = txt("Isso sugere um método.", T_MAIN, color=GREY).move_to(P3(0, 3.25))
        self.play(FadeIn(hd), run_time=0.5)
        passos = ("1. Sistema e intervalo", "2. Eixo e sinais", "3. Hipótese da conservação",
                  "4. Condição adicional", "5. Checagem")
        nos = VGroup(*[txt(p, T_MAIN) for p in passos]).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(P3(-4.2, 0.0))
        XI = 3.3

        def ilustra(k):
            if k == 0:
                b1 = Corpo("1", C1F, C1, 0.7, size=34).at(XI - 0.9, 0.3)
                b2 = Corpo("2", C2F, C2, 0.6, size=34).at(XI + 0.5, 0.3)
                g = VGroup(Line(P3(XI - 2.3, 0.3), P3(XI + 2.3, 0.3), color=STEEL, stroke_width=3), b1, b2)
                g.add(contorno(VGroup(b1, b2), buff=0.25))
                g.add(txt("pêndulo: A → B ou B → C", T_LAB, color=GREY).move_to(P3(XI, -0.75)))
                return g
            if k == 1:
                a = arrow(P3(XI - 1.2, 0.6), P3(XI + 1.2, 0.6), color=GREY, width=4)
                b = arrow(P3(XI + 0.6, -0.4), P3(XI - 0.6, -0.4), width=6)
                return VGroup(a, MathTex("+x", font_size=40, color=GREY).next_to(a, RIGHT, buff=0.12), b,
                              M("v", "<", "0", size=M_LAB).next_to(b, DOWN, buff=0.12))
            if k == 2:
                return VGroup(M(r"J_{\mathrm{ext},x}\approx 0", size=M_MID),
                              M(r"\Rightarrow\ P_x\ \text{conservado}", size=M_MID)).arrange(DOWN, buff=0.2).move_to(P3(XI, 0.1))
            if k == 3:
                return VGroup(M(r"\text{elástica}\ \rightarrow\ ", "K_i", "=", "K_f", size=M_LAB),
                              M(r"\text{ficam juntos}\ \rightarrow\ ", "v_1", "=", "v_2", size=M_LAB),
                              M(r"\text{só ``inelástica''}\ \rightarrow\ \text{falta informação}", size=M_LAB, color=MAG)
                              ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(P3(XI, 0.1))
            return VGroup(txt("unidades · sinais · energia", T_LAB, color=GREY),
                          txt("casos-limite · nova etapa física?", T_LAB, color=GREY)).arrange(DOWN, buff=0.18).move_to(P3(XI, 0.1))

        atual = None
        for k in range(5):
            il = ilustra(k)
            anims = [FadeIn(nos[k])] + [nos[j].animate.set_opacity(0.4) for j in range(k)]
            if atual is not None:
                anims.append(FadeOut(atual))
            self.play(*anims, FadeIn(il), run_time=0.7)
            atual = il
            self.wait(2.2 if k in (0, 3) else 1.6)
        self.play(FadeOut(atual), FadeOut(nos), FadeOut(hd), run_time=0.5)
        sint = txt("sistema + intervalo + conservação válida + condição suficiente", 33, color=CYAN).move_to(P3(0, 0.3))
        self.play(FadeIn(sint, scale=0.96), Create(box(sint, buff=0.22)), run_time=0.9)
        self.wait(2.2)
        self.clear()

        # Ponte: colisão oblíqua em um plano (massas iguais; u1 = (2,0), u2 = 0 → v1 = (1,−1), v2 = (1,1))
        R, KX = 0.42, 1.0
        grade = VGroup(*[Line(P3(x, -2.6), P3(x, 1.9), color=STEEL, stroke_width=1, stroke_opacity=0.35)
                         for x in np.arange(-6.5, 7.0, 1.0)],
                       *[Line(P3(-6.8, y), P3(6.8, y), color=STEEL, stroke_width=1, stroke_opacity=0.35)
                         for y in np.arange(-2.5, 2.0, 1.0)])
        c1 = P3(-0.3, -0.6)                                       # centro do disco 1 no contato
        nrm = np.array([np.cos(PI / 4), np.sin(PI / 4), 0.0])     # linha dos centros no contato
        c2 = c1 + 2 * R * nrm                                     # disco 2 parado ali
        t = ValueTracker(-1.8)
        u1v, v1v, v2v = np.array([2.0, 0, 0]), np.array([1.0, -1.0, 0]), np.array([1.0, 1.0, 0])

        def pos():
            tv = t.get_value()
            if tv <= 0:
                return c1 + u1v * tv * KX, c2
            return c1 + v1v * tv * KX, c2 + v2v * tv * KX

        def disco(cor_f, cor_s, nome):
            return VGroup(Circle(radius=R, stroke_color=cor_s, stroke_width=3, fill_color=cor_f, fill_opacity=0.45),
                          MathTex(nome, font_size=34, color=WHITE_))

        d1, d2 = disco(C1F, C1, "1"), disco(C2F, C2, "2")
        d1.add_updater(lambda m: m.move_to(pos()[0]))
        d2.add_updater(lambda m: m.move_to(pos()[1]))
        d1.move_to(pos()[0])
        d2.move_to(pos()[1])

        def vetores():
            tv = t.get_value()
            p1, p2 = pos()
            ka = 0.55
            def borda(p, v):
                return p + v / np.linalg.norm(v) * R
            if tv <= 0:
                a = arrow(borda(p1, u1v), borda(p1, u1v) + u1v * ka, width=5, tip=0.18)
                return VGroup(a, MathTex(r"\vec u_1", font_size=36, color=C1).next_to(a.get_end(), UP, buff=0.08))
            a1 = arrow(borda(p1, v1v), borda(p1, v1v) + v1v * ka, width=5, tip=0.18)
            a2 = arrow(borda(p2, v2v), borda(p2, v2v) + v2v * ka, width=5, tip=0.18)
            return VGroup(a1, a2, MathTex(r"\vec v_1", font_size=36, color=C1).next_to(a1.get_end(), DOWN, buff=0.08),
                          MathTex(r"\vec v_2", font_size=36, color=C2).next_to(a2.get_end(), RIGHT, buff=0.1))

        vs = always_redraw(vetores)
        ev = M(r"\vec P_i", "=", r"\vec P_f", size=M_MAIN, color=CYAN).move_to(P3(0, 3.2))
        self.play(FadeIn(grade), FadeIn(d1), FadeIn(d2), FadeIn(vs), FadeIn(ev), run_time=0.9)
        no = txt("sem trilho: um plano, contato oblíquo", T_SMALL, color=DIM).move_to(P3(0, -3.0))
        self.play(FadeIn(no), run_time=0.4)
        self.play(t.animate.set_value(0.0), rate_func=linear, run_time=1.6)
        self.play(Flash(c1 + R * nrm, color=WHITE_, line_length=0.2, flash_radius=0.1, num_lines=10, run_time=0.35))
        t.set_value(1e-5)
        self.play(t.animate.set_value(1.0), rate_func=linear, run_time=1.2)
        self.wait(0.8)
        q = txt("E quando os corpos podem sair em direções diferentes?", T_MAIN, color=GREY).move_to(P3(0, 2.4))
        self.play(FadeIn(q), run_time=0.6)
        self.wait(1.4)
        prox = txt("PRÓXIMO: COLISÕES EM DUAS DIMENSÕES", 44).move_to(P3(0, -3.45))
        self.play(FadeOut(no), FadeIn(prox, shift=0.1 * UP), run_time=0.8)
        self.wait(2.6)
        for m in (d1, d2, vs):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.wm], run_time=1.0)
        self.wait(0.6)
