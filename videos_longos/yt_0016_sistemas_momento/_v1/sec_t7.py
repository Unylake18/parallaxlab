"""Lote P7: T7 — sistemas de partículas (Moysés §8.1–8.3). Três esferas numa fronteira; dp_i/dt → soma → matriz de pares
(cada par aparece duas vezes e se apaga) → dP/dt = F_ext; binário; componentes; linha qualitativa do campo."""
from kit import *  # noqa: F401,F403

R = 0.68
Y_CHAO = -1.7
XC = -4.6
C1, C3 = P3(XC - R, Y_CHAO + R), P3(XC + R, Y_CHAO + R)
C2 = P3(XC, Y_CHAO + R + 2 * R * math.sin(PI / 3))
PARES = ((1, 2), (1, 3), (2, 3))


def esfera(n, cor):
    b = bola(R, cor)
    b.add(MathTex(str(n), font_size=40, color=BACKGROUND_COLOR if cor == GEO else WHITE_).move_to(b))
    return b


def contato(ca, cb, L=0.42):
    """Par de forças de contato iguais e opostas no ponto de contato entre a e b (empurram cada uma para dentro da sua esfera)."""
    c = (ca + cb) / 2
    u = (cb - ca) / np.linalg.norm(cb - ca)
    return VGroup(arrow(c, c - L * u, color=FC, width=3.5, tip=0.13, z=9), arrow(c, c + L * u, color=FC, width=3.5, tip=0.13, z=9))


class LoteT7(Base):
    def construct(self):
        self.setup_base(cap="SISTEMAS DE PARTÍCULAS", selo="MOYSÉS §8.1–8.3")
        self.t7_1()
        self.t7_2_3()
        self.t7_4_5()
        self.t7_6()
        self.t7_7()
        self.fim()
        self.relatorio()

    # ── T7-1 ────────────────────────────────────────────────────────────────────────────────────────────────
    def aparato(self):
        s1, s2, s3 = esfera(1, STEEL), esfera(2, GEO), esfera(3, STEEL)
        s1.move_to(C1), s2.move_to(C2), s3.move_to(C3)
        piso = chao(-7.0, -2.2, Y_CHAO)
        fr = fronteira(3.3, 2.7, P3(XC, (Y_CHAO + 0.08 + C2[1] + R + 0.22) / 2), rotulo="SISTEMA")
        internas = VGroup(contato(C1, C2), contato(C1, C3), contato(C2, C3))
        ext = VGroup()
        for c in (C1, C2, C3):
            ext.add(arrow(c, c + P3(0, -0.42), color=FC, width=6, tip=0.15, z=10))
        for c in (C1, C3):
            ext.add(arrow(P3(c[0], Y_CHAO - 0.85), P3(c[0], Y_CHAO - 0.02), color=FC, width=6, tip=0.17, z=10))
        lN = tex(r"\vec N", FC, 34).move_to(P3(XC, Y_CHAO - 0.5))
        lP = tex(r"m\vec g", FC, 30).move_to(C1 + P3(-R - 0.45, 0.05)).set_z_index(12)
        return VGroup(s1, s2, s3), piso, fr, internas, ext, VGroup(lN, lP)

    def t7_1(self):
        self.an("T7-1")
        esf, piso, fr, intn, ext, lext = self.aparato()
        self.ap = VGroup(esf, piso, fr, intn, ext, lext)
        self.esf, self.intn, self.ext, self.fr = esf, intn, ext, fr
        self.play(FadeIn(piso), LaggedStart(*[FadeIn(s, scale=0.85) for s in esf], lag_ratio=0.2), run_time=1.2)
        self.ate(0.12)
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=1.2)
        self.ate(0.38)
        li = VGroup(arrow(P3(-2.0, 0.75), P3(-1.4, 0.75), color=FC, width=3.5, tip=0.13), txt("INTERNAS", T_SMALL, color=FC))
        li[1].next_to(li[0], RIGHT, buff=0.15)
        self.play(LaggedStart(*[GrowArrow(a) for par in intn for a in par], lag_ratio=0.08), FadeIn(li), run_time=1.4)
        self.ate(0.6)
        le = VGroup(arrow(P3(-2.0, -0.05), P3(-1.4, -0.05), color=FC, width=6, tip=0.17), txt("EXTERNAS", T_SMALL, color=FC))
        le[1].next_to(le[0], RIGHT, buff=0.15)
        self.play(LaggedStart(*[GrowArrow(a) for a in ext], lag_ratio=0.1), FadeIn(lext), FadeIn(le), run_time=1.4)
        self.leg = VGroup(li, le)
        self.ap.add(self.leg)
        self.ate(0.97)

    # ── T7-2, T7-3 ──────────────────────────────────────────────────────────────────────────────────────────
    def t7_2_3(self):
        self.an("T7-2")
        e1 = Mc((r"\frac{d\vec p_i}{dt}", MAG), "=", r"\sum_j", (r"\vec F_{i(j)}", FC), "+", (r"\vec F_i^{\,ext}", FC), size=58).move_to(P3(3.9, 1.5))
        self.play(self.esf[0].animate.set_color(GEO).set_opacity(1), run_time=0.4)
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=1.0)
        self.ate(0.45)
        b1 = Brace(VGroup(e1[2], e1[3]), DOWN, buff=0.12, color=DIM)
        b2 = Brace(e1[5], DOWN, buff=0.12, color=DIM).align_to(b1, UP)
        l1 = txt("INTERNAS", 20, color=DIM).next_to(b1, DOWN, buff=0.1)
        l2 = txt("EXTERNA", 20, color=DIM).next_to(b2, DOWN, buff=0.1)
        leg = linha(tex("i", WHITE_, 34), "RECEBE DE", tex("j", WHITE_, 34), size=22, buff=0.14).move_to(P3(3.9, -0.45))
        self.play(GrowFromCenter(b1), FadeIn(l1), run_time=0.7)
        self.ate(0.7)
        self.play(GrowFromCenter(b2), FadeIn(l2), FadeIn(leg), run_time=0.7)
        self.ate(0.97)
        # T7-3 -----------------------------------------------------------------------------------------------
        self.an("T7-3")
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(l1), FadeOut(l2), FadeOut(leg), run_time=0.4)
        e2 = Mc((r"\frac{d\vec P}{dt}", MAG), "=", r"\sum_i", r"\sum_j", (r"\vec F_{i(j)}", FC), "+", (r"\vec F^{\,ext}", FC), size=58) \
            .move_to(P3(3.9, 1.5))
        self.play(TransformMatchingTex(e1, e2), run_time=1.4)
        pd = Mc((r"\vec P", MAG), "=", (r"\sum_i \vec p_i", MAG), size=46).move_to(P3(3.9, -0.1))
        self.ate(0.3)
        self.play(FadeIn(pd, shift=0.1 * UP), run_time=0.8)
        self.ate(0.6)
        b1 = Brace(VGroup(e2[2], e2[4]), DOWN, buff=0.12, color=DIM)
        b2 = Brace(e2[6], DOWN, buff=0.12, color=DIM).align_to(b1, UP)
        l1 = txt("SOMA DUPLA DAS INTERNAS", 20, color=DIM).next_to(b1, DOWN, buff=0.1)
        l2 = txt("EXTERNA TOTAL", 20, color=DIM).next_to(b2, DOWN, buff=0.1)
        pd.generate_target().move_to(P3(3.9, -1.0))
        self.play(MoveToTarget(pd), GrowFromCenter(b1), FadeIn(l1), GrowFromCenter(b2), FadeIn(l2), run_time=0.9)
        self.e2, self.pd, self.br = e2, pd, VGroup(b1, b2, l1, l2)
        self.ate(0.97)

    # ── T7-4, T7-5 ──────────────────────────────────────────────────────────────────────────────────────────
    def t7_4_5(self):
        self.an("T7-4")
        self.play(FadeOut(self.ap), FadeOut(self.br), FadeOut(self.pd), run_time=0.6)
        X = {1: -4.9, 2: -3.5, 3: -2.1}
        Y = {1: 0.75, 2: -0.35, 3: -1.45}
        cw, chh = 1.4, 1.1
        grade = VGroup()
        cel = {}
        for i in (1, 2, 3):
            for j in (1, 2, 3):
                r = Rectangle(width=cw, height=chh).move_to(P3(X[j], Y[i])).set_stroke(DIM, 1.5, opacity=0.6)
                grade.add(r)
                if i == j:
                    cel[i, j] = tex(r"\cdot", DIM, 40).move_to(r)
                else:
                    cel[i, j] = tex(rf"\vec F_{{{i}({j})}}", WHITE_, 38).move_to(r)
        cols = VGroup(*[tex(f"{j}", DIM, 36).move_to(P3(X[j], 1.6)) for j in (1, 2, 3)])
        rows = VGroup(*[tex(f"{i}", DIM, 36).move_to(P3(-5.95, Y[i])) for i in (1, 2, 3)])
        lc = txt("COLUNA: QUEM FAZ", 20, color=DIM).move_to(P3(-3.5, 2.1))
        lr = txt("LINHA: QUEM RECEBE", 20, color=DIM).rotate(PI / 2).move_to(P3(-6.55, -0.35))
        self.play(Create(grade), FadeIn(cols), FadeIn(rows), FadeIn(lc), FadeIn(lr), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(c) for c in cel.values()], lag_ratio=0.06), run_time=1.2)
        self.ate(0.36)
        caixas = {}
        for k in cel:
            caixas[k] = SurroundingRectangle(cel[k], buff=0.12, corner_radius=0.08).set_stroke(FC, 3).set_fill(FC, 0.12)
        self.play(cel[1, 2].animate.set_color(FC), FadeIn(caixas[1, 2]), run_time=0.6)
        self.ate(0.47)
        self.play(cel[2, 1].animate.set_color(FC), FadeIn(caixas[2, 1]), run_time=0.6)
        soma = Mc((r"\vec F_{1(2)}", FC), "+", (r"\vec F_{2(1)}", FC), "=", "0", size=44).move_to(P3(-3.5, -2.55))
        self.ate(0.56)
        self.play(FadeIn(soma, shift=0.1 * UP), run_time=0.7)
        self.ate(0.66)

        def apaga(i, j, rt=0.7):
            self.play(*[cel[k].animate.set_opacity(0.13) for k in ((i, j), (j, i))], *[FadeOut(caixas[k]) for k in ((i, j), (j, i))],
                      run_time=rt)

        apaga(1, 2)
        for (i, j), fr in (((1, 3), 0.74), ((2, 3), 0.83)):
            self.ate(fr)
            nova = Mc((rf"\vec F_{{{i}({j})}}", FC), "+", (rf"\vec F_{{{j}({i})}}", FC), "=", "0", size=44).move_to(soma)
            self.play(cel[i, j].animate.set_color(FC), cel[j, i].animate.set_color(FC), FadeIn(caixas[i, j]), FadeIn(caixas[j, i]),
                      FadeOut(soma), FadeIn(nova), run_time=0.6)
            soma = nova
            self.wait(0.4)
            apaga(i, j, 0.6)
        self.ate(0.9)
        e3 = Mc((r"\frac{d\vec P}{dt}", MAG), "=", "0", "+", (r"\vec F^{\,ext}", FC), size=58).move_to(self.e2)
        dupla = VGroup(self.e2[2], self.e2[3], self.e2[4])
        self.play(dupla.animate.set_opacity(0.25), run_time=0.4)
        self.play(TransformMatchingTex(self.e2, e3), FadeOut(soma), run_time=1.0)
        self.ate(0.97)
        # T7-5 -----------------------------------------------------------------------------------------------
        self.an("T7-5")
        e4 = Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F^{\,ext}", FC), size=M_MAIN).move_to(P3(3.6, 1.2))
        self.play(FadeOut(grade), FadeOut(cols), FadeOut(rows), FadeOut(lc), FadeOut(lr), *[FadeOut(c) for c in cel.values()],
                  run_time=0.6)
        self.play(TransformMatchingTex(e3, e4), run_time=1.0)
        cx = SurroundingRectangle(e4, buff=0.25, corner_radius=0.12).set_stroke(MAG, 3)
        self.play(Create(cx), run_time=0.7)
        # o aparato volta: as internas somem, as externas ficam
        self.ap.remove(self.leg)
        self.intn.set_opacity(1)
        self.play(FadeIn(self.ap), run_time=0.7)
        self.ate(0.3)
        self.play(self.intn.animate.set_opacity(0.0), run_time=1.2)
        self.ate(0.62)
        d = dica("PRIMEIRO DEFINA O SISTEMA.", "SÓ FORÇA EXTERNA ENTRA NA VARIAÇÃO", "DO MOMENTO TOTAL")
        self.dica_entra(d)
        self.e4, self.cx = e4, cx
        self.ate(0.97)

    # ── T7-6 ────────────────────────────────────────────────────────────────────────────────────────────────
    def t7_6(self):
        self.an("T7-6")
        self.dica_sai()
        self.play(FadeOut(self.ap), FadeOut(self.e4), FadeOut(self.cx), run_time=0.6)
        l1 = linha("SE A FORÇA EXTERNA RESULTANTE", tex("=0", WHITE_, 40), size=28, buff=0.15)
        l2 = linha(tex(r"\Rightarrow", WHITE_, 40), tex(r"\vec P", MAG, 46), "CONSTANTE", size=28, buff=0.2)
        VGroup(l1, l2).arrange(DOWN, buff=0.3).move_to(P3(3.4, 1.4))
        self.play(FadeIn(l1, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(l2, shift=0.1 * UP), run_time=0.7)
        self.ate(0.42)
        oc, r = P3(-3.6, -0.5), 1.35
        ang = ValueTracker(0.0)

        def disco():
            a = ang.get_value()
            g = VGroup(Circle(radius=r, arc_center=oc).set_stroke(mix(STEEL, 0.5), 2.5).set_fill(STEEL, 1),
                       Circle(radius=r * 0.82, arc_center=oc).set_stroke(WHITE_, 1, opacity=0.3))
            g.add(AnnularSector(inner_radius=0.25, outer_radius=r * 0.8, angle=0.55, start_angle=a, arc_center=oc)
                  .set_stroke(width=0).set_fill(GEO, 0.55))
            g.add(AnnularSector(inner_radius=0.25, outer_radius=r * 0.8, angle=0.55, start_angle=a + PI, arc_center=oc)
                  .set_stroke(width=0).set_fill(GEO, 0.55))
            g.add(Dot(oc, radius=0.09, color=WHITE_).set_z_index(9))
            return g
        dg = always_redraw(disco)
        fa = arrow(oc + P3(-0.15, r), oc + P3(1.45, r), color=FC, width=7, tip=0.22, z=10)
        fb = arrow(oc + P3(0.15, -r), oc + P3(-1.45, -r), color=FC, width=7, tip=0.22, z=10)
        la = tex(r"\vec F", FC, 38).next_to(fa, UP, buff=0.1)
        lb = tex(r"-\vec F", FC, 38).next_to(fb, DOWN, buff=0.1)
        self.play(FadeIn(dg), run_time=0.7)
        self.play(GrowArrow(fa), GrowArrow(fb), FadeIn(la), FadeIn(lb), run_time=0.8)
        t0 = self.clk.get_value()
        ang.add_updater(lambda m: m.set_value(-0.35 * (self.clk.get_value() - t0) ** 1.3))
        self.add(ang)
        n1 = txt("O CENTRO NÃO SAI DO LUGAR", 20, color=DIM).move_to(oc + P3(0, -2.25))
        n2 = linha(tex(r"\vec P", MAG, 40), "NÃO MUDA, MAS O DISCO GIRA", size=24, buff=0.18).move_to(P3(3.4, -0.6))
        self.ate(0.62)
        self.play(FadeIn(n1), run_time=0.6)
        self.ate(0.75)
        self.play(FadeIn(n2, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        ang.clear_updaters()
        self.remove(ang)
        dg.clear_updaters()

    # ── T7-7 ────────────────────────────────────────────────────────────────────────────────────────────────
    def t7_7(self):
        self.an("T7-7")
        self.clear(rt=0.6)
        cx = Mc((r"\frac{dP_x}{dt}", MAG), "=", (r"F^{\,ext}_x", FC), size=M_MAIN).move_to(P3(3.8, 1.75))
        cy = Mc((r"\frac{dP_y}{dt}", MAG), "=", (r"F^{\,ext}_y", FC), size=M_MAIN).move_to(P3(3.8, 0.15))
        nota = txt("COMPONENTE POR COMPONENTE", T_SMALL, color=DIM).move_to(P3(3.8, -0.95))
        self.play(FadeIn(cx, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(cy, shift=0.1 * UP), FadeIn(nota), run_time=0.8)
        # à esquerda: corpo lançado; força externa só vertical → componente horizontal do momento constante
        X0, Y0, VX, VY, G = -6.3, -1.9, 1.15, 2.6, 1.3
        piso = chao(-7.0, -0.6, Y0 - 0.2)
        cam = DashedVMobject(VMobject().set_points_smoothly([P3(X0 + VX * t, Y0 + VY * t - G * t * t / 2) for t in np.linspace(0, 4.0, 40)])
                             .set_stroke(DIM, 2, opacity=0.5), num_dashes=40)
        tt = ValueTracker(0.0)

        def corpo():
            t = tt.get_value()
            c = P3(X0 + VX * t, Y0 + VY * t - G * t * t / 2)
            vy = VY - G * t
            g = VGroup(bola(0.2, STEEL).move_to(c))
            g.add(arrow(c, c + P3(0.75 * VX, 0), color=MAG, width=5, tip=0.15, z=9))
            if abs(vy) > 0.08:
                g.add(arrow(c, c + P3(0, 0.38 * vy), color=MAG, width=5, tip=0.15, z=9, op=0.55))
            g.add(arrow(c + P3(0, -0.25), c + P3(0, -0.95), color=FC, width=5, tip=0.15, z=9))
            return g
        cg = always_redraw(corpo)
        lpx = tex(r"P_x", MAG, 34).move_to(P3(-5.7, 1.4))
        lfe = linha(tex(r"F^{\,ext}", FC, 32), "SÓ NA VERTICAL", size=20, buff=0.12).move_to(P3(-3.6, 2.15))
        self.ate(0.12)
        self.play(FadeIn(piso), Create(cam), FadeIn(cg), FadeIn(lfe), run_time=1.0)
        self.play(tt.animate.set_value(4.0), run_time=6.0, rate_func=linear)
        res = linha(tex(r"P_x", MAG, 40), "SE CONSERVA", size=26, buff=0.18).move_to(P3(-3.6, -2.95))
        self.play(FadeIn(res, shift=0.1 * UP), run_time=0.7)
        self.ate(0.42)
        cg.clear_updaters()
        # linha qualitativa: cargas em movimento e o momento do campo
        campo = linha("MOMENTO DAS PARTÍCULAS", tex("+", DIM, 32), "MOMENTO DO CAMPO", tex("=", DIM, 32), "CONSTANTE", size=17, color=DIM,
                      buff=0.12).move_to(P3(3.6, -2.95))
        q1 = VGroup(Circle(radius=0.16).set_stroke(GEO, 2).set_fill(STEEL, 1), tex("+", WHITE_, 26)).move_to(P3(2.6, -2.15))
        q2 = VGroup(Circle(radius=0.16).set_stroke(GEO, 2).set_fill(STEEL, 1), tex("+", WHITE_, 26)).move_to(P3(4.4, -2.0))
        v1 = arrow(P3(2.8, -2.15), P3(3.4, -2.15), color=VEL, width=4, tip=0.12)
        v2 = arrow(P3(4.4, -1.8), P3(4.4, -1.4), color=VEL, width=4, tip=0.12)
        self.ate(0.58)
        self.play(FadeIn(q1), FadeIn(q2), GrowArrow(v1), GrowArrow(v2), run_time=0.8)
        self.play(FadeIn(campo, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        self.clear(rt=0.5)
