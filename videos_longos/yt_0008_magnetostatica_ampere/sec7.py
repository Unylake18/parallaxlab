"""N21–N23: eletrostática × magnetostática (com qualificadores), síntese das quatro geometrias e o gancho B = ∇×A."""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, Circle, Rectangle, RoundedRectangle, FadeIn, FadeOut, Create, Indicate, LaggedStart,
    DashedVMobject, VMobject, Transform, ReplacementTransform, TransformFromCopy, Write, linear, smooth, UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import TAU


class Sec7:
    # ── N21 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def comparacao(self):
        self.section("comparacao", "Eletrostática × magnetostática")
        self.clear()
        cols = []
        for cx, title, col, divt, rott, qual in [
            (-3.6, "ELETROSTÁTICA", CYAN, (r"\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}", r"\mathbf E", r"\rho"),
             (r"\nabla\times\mathbf E=\mathbf 0", r"\mathbf E"), "na eletrostática"),
            (3.6, "MAGNETOSTÁTICA", MAG, (r"\nabla\cdot\mathbf B=0", r"\nabla\cdot\mathbf B"), (r"\nabla\times\mathbf B=\mu_0\mathbf J", r"\nabla\times\mathbf B", r"\mathbf J"),
             "na magnetostática")]:
            pn = panel(6.4, 4.7, [cx, -0.05, 0])
            tt = txt(title, 30, col).move_to([cx, 1.85, 0])
            d = E(*divt, size=M_L).move_to([cx, 0.85, 0])
            r = E(*rott, size=M_L).move_to([cx - 0.55, -0.6, 0])
            q = txt(qual, T_NOTE, DIM).next_to(r, DOWN, buff=0.18)
            bx = box(VGroup(r, q), col, buff=0.15)
            ph = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=0.95, height=0.8, color=WHITE, stroke_width=2).move_to(bx.get_right() + [0.62, 0, 0]),
                                num_dashes=18).set_opacity(0.35)
            pq = E("+\\,?", size=M_M).move_to(ph).set_opacity(0.35)
            cols.append(VGroup(pn, tt, d, r, q, bx, ph, pq))
        for c in cols:
            self.play(FadeIn(c[0]), FadeIn(c[1]), run_time=0.6)
            self.play(FadeIn(c[2], shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(c[3], shift=UP * 0.1), FadeIn(c[4]), run_time=0.8)
            self.play(Create(c[5]), run_time=0.5)
            self.hold(1.0)
        self.caption("Divergente: carga elétrica é fonte de $\\mathbf E$; não existe fonte de $\\mathbf B$")
        self.play(Indicate(cols[0][2], color=CYAN, scale_factor=1.05), Indicate(cols[1][2], color=MAG, scale_factor=1.05), run_time=1.2)
        self.hold(2.0)
        self.caption("Rotacional: $\\mathbf E$ eletrostático não circula; $\\mathbf B$ circula em torno da corrente")
        self.play(Indicate(cols[0][3], color=CYAN, scale_factor=1.05), Indicate(cols[1][3], color=MAG, scale_factor=1.05), run_time=1.2)
        self.hold(2.0)
        self.caption("Estas formas do rotacional valem para campos que não variam no tempo")
        self.mark("n21_comparacao")
        self.hold(4.0)
        self.play(*[FadeOut(c) for c in cols], run_time=0.8)

    # ── N22 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def sintese(self):
        self.section("sintese", "Quatro geometrias, uma estratégia")
        xs = [-5.4, -1.8, 1.8, 5.4]
        icons = VGroup()
        # fio (de cima)
        c = np.array([xs[0], 0.95, 0])
        icons.add(VGroup(self.out_symbol(c, 1, 0.14, GREEN), DashedVMobject(Circle(radius=0.8, color=VIOLET, stroke_width=3).move_to(c), num_dashes=24),
                         *[arrow(c + 0.8 * np.array([math.cos(t), math.sin(t), 0]), c + 0.8 * np.array([math.cos(t), math.sin(t), 0]) + 0.4 * np.array([-math.sin(t), math.cos(t), 0]),
                                 MAG, 3.5, tip=0.13) for t in (0.3, 2.4, 4.4)]))
        # lâmina (de perfil)
        c = np.array([xs[1], 0.95, 0])
        icons.add(VGroup(*[self.out_symbol(c + [x, 0, 0], 1, 0.08, GREEN) for x in np.linspace(-1.2, 1.2, 9)],
                         Rectangle(width=0.9, height=1.3, color=VIOLET, stroke_width=3).move_to(c),
                         arrow(c + [0.35, 0.85, 0], c + [-0.35, 0.85, 0], MAG, 3.5, tip=0.13), arrow(c + [-0.35, -0.85, 0], c + [0.35, -0.85, 0], MAG, 3.5, tip=0.13)))
        # solenoide (corte)
        c = np.array([xs[2], 0.95, 0])
        icons.add(VGroup(*[self.out_symbol(c + [x, 0.45, 0], 1, 0.08, GREEN) for x in np.linspace(-1.2, 1.2, 8)],
                         *[self.out_symbol(c + [x, -0.45, 0], -1, 0.08, GREEN) for x in np.linspace(-1.2, 1.2, 8)],
                         Rectangle(width=0.9, height=0.75, color=VIOLET, stroke_width=3).move_to(c + [0, 0.5, 0]),
                         arrow(c + [-0.5, -0.05, 0], c + [0.5, -0.05, 0], MAG, 3.5, tip=0.13)))
        # toroide (de cima)
        c = np.array([xs[3], 0.95, 0])
        icons.add(VGroup(Circle(radius=0.5, color=BLUE_L, stroke_width=1.5).move_to(c).set_stroke(opacity=0.5), Circle(radius=1.0, color=BLUE_L, stroke_width=1.5).move_to(c).set_stroke(opacity=0.5),
                         *[self.out_symbol(c + 0.5 * np.array([math.cos(t), math.sin(t), 0]), 1, 0.06, GREEN) for t in np.linspace(0, TAU, 10, endpoint=False)],
                         *[self.out_symbol(c + 1.0 * np.array([math.cos(t), math.sin(t), 0]), -1, 0.06, GREEN) for t in np.linspace(0, TAU, 10, endpoint=False)],
                         DashedVMobject(Circle(radius=0.75, color=VIOLET, stroke_width=3).move_to(c), num_dashes=24)))
        forms = [E(r"B=\frac{\mu_0 I}{2\pi s}", "B", "I", size=M_M), E(r"B=\frac{\mu_0 K}{2}", "B", "K", size=M_M), E(r"B=\mu_0 nI", "B", "I", size=M_M),
                 E(r"B=\frac{\mu_0 NI}{2\pi s}", "B", "NI", size=M_M)]
        names = ["fio · fora", "lâmina", "solenoide ideal · interior", "toroide ideal · $a<s<b$"]       # domínios de validade na tela
        for i, f in enumerate(forms):
            f.move_to([xs[i], -1.0, 0])
        nms = VGroup(*[rich(n, 22, DIM).move_to([xs[i], -1.85, 0]) for i, n in enumerate(names)])
        self.play(LaggedStart(*[FadeIn(ic) for ic in icons], lag_ratio=0.2), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(f) for f in forms], lag_ratio=0.2), FadeIn(nms), run_time=1.4)
        self.caption("Fio, lâmina, solenoide, toroide: em todos, a simetria escolheu o caminho")
        self.mark("n22_quatro")
        self.hold(4.0)
        # reduz o foco
        grp = VGroup(icons, VGroup(*forms), nms)
        self.play(grp.animate.scale(0.5).move_to([0, 1.75, 0]).fade(0.55), run_time=1.4)
        chain = E(r"\text{simetria}\ \longrightarrow\ \text{caminho}\ \longrightarrow\ \text{circulação}", size=M_L)
        chain.move_to([0, -0.15, 0])
        root = E(r"\nabla\times\mathbf B=\mu_0\mathbf J", r"\nabla\times\mathbf B", r"\mathbf J", size=M_L).move_to([0, -1.55, 0])
        rb = box(root, MAG)
        cb = box(chain, WHITE)
        self.play(FadeIn(chain), Create(cb), run_time=1.0)
        self.play(FadeIn(root), Create(rb), run_time=0.8)
        self.caption("Não é decorar quatro campos: é ver por que existe um caminho que simplifica a integral")
        self.mark("n22_estrategia")
        self.hold(5.0)
        self.play(FadeOut(VGroup(grp, chain, cb, rb)), root.animate.move_to([0, 1.2, 0]), run_time=1.0)
        self.sint_root = root

    # ── N23 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def gancho(self):
        self.section("gancho", "Um campo com divergente sempre zero")
        root = self.sint_root
        d = E(r"\nabla\cdot\mathbf B=0", r"\nabla\cdot\mathbf B", size=M_XL).move_to([-2.6, 1.2, 0])
        self.play(FadeOut(root), FadeIn(d), run_time=1.0)
        self.caption("Como construir, automaticamente, um campo cujo divergente é sempre zero?")
        self.hold(2.5)
        idn = E(r"\nabla\cdot(\nabla\times\mathbf A)=0", r"\nabla\times\mathbf A", size=M_XL, colors={r"\nabla\times\mathbf A": WHITE}).move_to([-2.6, -0.4, 0])
        self.play(FadeIn(idn, shift=UP * 0.1), run_time=1.0)
        self.caption("Qualquer rotacional tem divergente zero")
        self.hold(2.0)
        # alinha: o ∇· da identidade sob o ∇· de B
        self.play(idn.animate.shift(RIGHT * (glyphs_left(d) - glyphs_left(idn))), run_time=0.8)
        hb = box(VGroup(*d[0][2:3]), MAG, buff=0.08)
        ha = box(glyphs(idn, r"\nabla\times\mathbf A", 0), WHITE, buff=0.08)
        self.play(Create(hb), Create(ha), run_time=0.8)
        self.hold(1.5)
        res = E(r"\mathbf B=\nabla\times\mathbf A", r"\mathbf B", r"\nabla\times\mathbf A", size=M_XL, colors={r"\nabla\times\mathbf A": WHITE}).move_to([3.7, 0.4, 0])
        self.play(TransformFromCopy(VGroup(*d[0][2:3]), glyphs(res, r"\mathbf B", 0)), TransformFromCopy(glyphs(idn, r"\nabla\times\mathbf A", 0), glyphs(res, r"\nabla\times\mathbf A", 0)),
                  FadeIn(VGroup(*[g for k, g in enumerate(res[0]) if k not in glyph_ids(res)])), run_time=1.8)
        self.remove(*res[0])
        self.add(res)
        rb = box(res, MAG)
        self.play(Create(rb), FadeOut(hb), FadeOut(ha), run_time=0.6)
        al = rich("$\\mathbf A$: potencial vetor magnético", T_NOTE).next_to(rb, DOWN, buff=0.35)
        self.play(FadeIn(al), run_time=0.8)
        self.caption("$\\mathbf A$ é o potencial vetor magnético")
        self.mark("n23_potencial_vetor")
        self.hold(4.0)
        self.delcap()
        self.out(d, idn, res, rb, al, self.head, rt=1.0)
        self.head = None

    # ── encerramento padrão dos longos (end card do yt_0005: marca, anéis tracejados, inscrição e próximo assunto) ──
    def cta(self):
        self.section("cta")
        oc = np.array([0.0, 0.5, 0.0])
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)), dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.16)
                         for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, s=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(s * dt, about_point=oc))
        logo = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png")).set_width(6.0).move_to(oc + np.array([0.0, 0.5, 0.0]))
        msg = txt("Inscreva-se para acompanhar os próximos vídeos", 28, opacity=0.9).move_to(oc + np.array([0.0, -0.9, 0.0]))
        nxt = VGroup(txt("Próximo:", 24, opacity=0.8), txt("o potencial vetor magnético", 24, opacity=0.95)).arrange(RIGHT, buff=0.2).move_to(oc + np.array([0.0, -1.75, 0.0]))

        def ripple():
            w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.35)
            self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.6)
            self.remove(w)

        self.play(FadeOut(self.wm), FadeOut(self.tag), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.0)
        self.hold(0.8)
        self.play(FadeIn(nxt, shift=0.1 * UP), run_time=1.0)
        self.mark("cta")
        ripple()
        ripple()
        self.hold(1.2)


def glyphs_left(m):
    return m[0][0].get_left()[0]


def glyph_ids(m):
    return {i for occs in m.tok.values() for o in occs for i in o}
