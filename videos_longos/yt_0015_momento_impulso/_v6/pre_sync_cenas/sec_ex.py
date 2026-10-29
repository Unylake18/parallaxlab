"""Lote PE: E1 (bola na parede), E2 (chute em 2D), E3 (força que cresce com o tempo). v3: PALCO (figura grande) + CONTA (dados,
álgebra, resultado em coluna), equações por Write, F⃗ saindo do ponto de contato, triângulo grande com F⃗_méd paralela por fora,
Riemann antes da primitiva no E3, DICAs."""
from kit import *  # noqa: F401,F403
from sec_teoria import foguete as foguete_t4

KP = 0.17                                   # u por kg·m/s no E1


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def eixo_x(x0, y, comp=1.2):
    return VGroup(Arrow(P3(x0, y), P3(x0 + comp, y), buff=0, color=DIM, stroke_width=3, tip_length=0.16),
                  tex("+x", DIM, 34).move_to(P3(x0 + comp + 0.4, y)))


def alvo_conta(*mobs, **kw):
    """Posições que os mobjects teriam numa coluna da CONTA (sem mexer nos originais)."""
    return [m.get_center() for m in conta(*[x.copy() for x in mobs], **kw)]


class LoteEx(Base):
    def construct(self):
        self.setup_base()
        self.e1()
        self.e2()
        self.e3()
        self.fim()
        self.relatorio()

    def bola_vel(self, x, y, comp, cor=VEL, w=6, r=0.38):
        b = bola(r).move_to(P3(x, y))
        a = arrow(P3(x, y), P3(x + comp[0], y + comp[1]), color=cor, width=w)
        return b, a

    # ── E1 ──────────────────────────────────────────────────────────────────────────────────────────────────
    def e1(self):
        self.secao("EXERCÍCIO 1 · BOLA NA PAREDE", "TEOREMA DO IMPULSO · COM SINAL")
        self.an("E1-1")
        PX = -6.3
        parede = Rectangle(width=0.55, height=5.0).set_stroke(GEO, 2.5).set_fill(STEEL, 1).move_to(P3(PX - 0.28, -0.25))
        ex = eixo_x(-2.4, 2.15)
        r1 = txt("ANTES", T_LAB, color=GEO).move_to(P3(-4.7, 1.95))
        r2 = txt("DEPOIS", T_LAB, color=GEO).move_to(P3(-3.4, -0.65))
        b1, a1 = self.bola_vel(-1.0, 1.1, (-2.9, 0))
        b2, a2 = self.bola_vel(-4.9, -1.5, (1.95, 0))
        t1 = tex(r"30\ \mathrm{m/s}", VEL, 40).next_to(a1, UP, buff=0.18)
        t2 = tex(r"20\ \mathrm{m/s}", VEL, 40).next_to(a2, UP, buff=0.18)
        d1, d2 = tex(r"m=0{,}40\ \mathrm{kg}", WHITE_, 46), tex(r"\Delta t=0{,}010\ \mathrm{s}", WHITE_, 46)
        conta(d1, d2, topo=2.2, buff=0.35)
        self.play(FadeIn(parede, shift=0.2 * RIGHT), FadeIn(ex), FadeIn(r1), FadeIn(b1, shift=0.4 * LEFT), run_time=0.7)
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.6)
        # v6 (G5): cada dado acende no desenho enquanto é escrito
        self.ate(0.14)
        self.play(Write(d1), Indicate(b1, color=WHITE_, scale_factor=1.25), run_time=0.9)
        self.ate(0.3)
        self.play(Indicate(t1, color=WHITE_, scale_factor=1.2), Indicate(a1, color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.ate(0.42)
        self.play(FadeIn(r2), FadeIn(b2, shift=0.4 * RIGHT), run_time=0.6)
        self.play(GrowArrow(a2), FadeIn(t2), run_time=0.6)
        self.ate(0.62)
        fl = flash(P3(PX, -1.5)).set_z_index(12)
        self.play(Write(d2), FadeIn(fl, scale=0.6), Indicate(parede, color=WHITE_, scale_factor=1.03), run_time=0.8)
        self.play(FadeOut(fl), run_time=0.3)
        self.ate(0.82)
        self.play(Indicate(ex, color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.ate(0.97)
        # E1-2 · sinais; p⃗ᵢ, p⃗_f e Δp⃗ em três linhas -------------------------------------------------------------
        self.an("E1-2")
        vi = Mc((r"v_i", VEL), "=", (r"-30\ \mathrm{m/s}", VEL), size=46)
        vf = Mc((r"v_f", VEL), "=", (r"+20\ \mathrm{m/s}", VEL), size=46)
        eqJ = Mc((r"J", JC), "=", r"0{,}40\,(20-(-30))", "=", (r"20\ \mathrm{N\cdot s}", JC), size=42)
        conta(d1, d2, vi, vf, eqJ, topo=2.2, buff=0.35)
        self.play(Write(vi), Indicate(a1, color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.play(Indicate(vi[2], color=WHITE_, scale_factor=1.15), Indicate(ex, color=WHITE_), run_time=0.9)
        self.play(Write(vf), Indicate(a2, color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.ate(0.3)
        o = P3(-1.2, -1.85)
        y2, y3 = o[1] - 0.55, o[1] - 1.1
        pi_ = arrow(o, o + P3(-12 * KP, 0), color=MAG, width=8)
        pf_ = arrow(P3(o[0], y2), P3(o[0] + 8 * KP, y2), color=MAG, width=8)
        dp = arrow(P3(o[0] - 12 * KP, y3), P3(o[0] + 8 * KP, y3), color=MAG, width=10)
        lpi = tex(r"\vec p_i", MAG, 42).next_to(pi_.get_end(), LEFT, buff=0.15).shift(DOWN * 0.14)    # folga da seta do DEPOIS
        lpf = tex(r"\vec p_f", MAG, 42).next_to(pf_.get_end(), RIGHT, buff=0.15)
        ldp = tex(r"\Delta\vec p", MAG, 42).next_to(dp.get_end(), RIGHT, buff=0.15)
        zero = DashedLine(P3(o[0], o[1] + 0.3), P3(o[0], y2 - 0.25), color=DIM, stroke_width=2)
        liga = VGroup(DashedLine(P3(o[0] - 12 * KP, o[1] - 0.1), P3(o[0] - 12 * KP, y3 + 0.1), color=DIM, stroke_width=2),
                      DashedLine(P3(o[0] + 8 * KP, y2 - 0.1), P3(o[0] + 8 * KP, y3 + 0.1), color=DIM, stroke_width=2))
        self.play(GrowArrow(pi_), FadeIn(zero), FadeIn(lpi), run_time=0.7)
        self.ate(0.35)
        self.play(GrowArrow(pf_), FadeIn(lpf), run_time=0.6)
        self.ate(0.4)
        self.play(FadeIn(liga), GrowArrow(dp), run_time=0.8)
        self.play(FadeIn(ldp), run_time=0.4)
        self.ate(0.62)
        self.play(Write(VGroup(*eqJ[0:3])), Indicate(dp, color=WHITE_, scale_factor=1.05), run_time=1.1)
        self.ate(0.8)
        self.play(Indicate(eqJ[2], color=WHITE_, scale_factor=1.08), run_time=0.8)
        self.ate(0.88)
        self.play(Write(VGroup(*eqJ[3:5])), run_time=0.7)
        self.play(Indicate(eqJ[4], color=WHITE_, scale_factor=1.2), Indicate(dp, color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.ate(0.97)
        # E1-3 · a conta sem sinal (riscada com um traço reto) ---------------------------------------------------------
        self.an("E1-3")
        errada = tex(r"0{,}40\,(20-30)=-4\ \mathrm{N\cdot s}", APAGADO, 42).next_to(eqJ, DOWN, buff=0.45, aligned_edge=LEFT)
        pq = legenda("A PAREDE PUXOU A BOLA?", T_MAIN, color=WHITE_)
        self.play(Write(errada), run_time=0.9)
        rsc = risco(errada, w=5)
        self.play(Create(rsc), run_time=0.6)
        self.play(FadeIn(pq), Indicate(a2, color=WHITE_, scale_factor=1.05), run_time=0.6)
        self.ate(0.97)
        # E1-4 · F⃗ sai da bola; o ANTES/DEPOIS sai para o mg não cair em cima do 20 m/s -----------------------------------------
        self.an("E1-4")
        esq = VGroup(r1, r2, b1, a1, t1, b2, a2, t2)
        self.play(*[FadeOut(m) for m in (errada, rsc, pq, pi_, pf_, dp, lpi, lpf, ldp, zero, liga, vi, vf, eqJ)], FadeOut(esq), run_time=0.5)
        bb = bola(0.48).move_to(P3(PX + 0.48, 0.2))
        fa = arrow(bb.get_right(), bb.get_right() + P3(3.4, 0), color=FC, width=10, tip=0.3)      # sai da bola, na altura do centro
        fl = tex(r"\vec F_{\mathrm{m\acute{e}d}}", FC, 48).next_to(fa.get_end(), UP, buff=0.18)
        peso = arrow(bb.get_bottom(), bb.get_bottom() + P3(0, -0.42), color=FC, width=4, tip=0.12)
        pl = tex(r"m g=3{,}9\ \mathrm{N}", FC, 34).next_to(peso, RIGHT, buff=0.2)
        fm = Mc((r"F_{\mathrm{m\acute{e}d}}", FC), "=", (r"\frac{20}{0{,}010}", JC), "=", (r"2.000\ \mathrm{N}", FC), size=50)
        q = txt("UMAS 500 VEZES O PESO", T_SMALL, color=GEO)
        conta(d1, d2, fm, q, topo=2.2, buff=0.45)
        self.play(FadeIn(bb), run_time=0.4)
        self.play(GrowArrow(fa), run_time=0.8)
        self.play(FadeIn(fl), Write(fm), Indicate(fa, color=WHITE_, scale_factor=1.04), run_time=1.0)
        self.ate(0.55)
        self.play(GrowArrow(peso), FadeIn(pl), FadeIn(q), run_time=0.8)
        self.play(Indicate(fm[4], color=WHITE_, scale_factor=1.15), Indicate(peso, color=WHITE_), run_time=0.8)
        self.ate(0.97)
        # E1-5 · parar × rebater + DICA (o ANTES/DEPOIS volta ao PALCO) -------------------------------------------------------
        self.an("E1-5")
        self.play(*[FadeOut(m) for m in (fa, fl, peso, pl, fm, q, d1, d2, bb)], run_time=0.5)
        self.play(FadeIn(esq), run_time=0.5)
        zx, k = 4.6, KP
        grp = VGroup()
        for y, nome, extra in ((1.55, "PARAR", False), (-0.35, "REBATER", True)):
            r = txt(nome, T_LAB, bold=True).move_to(P3(1.75, y))
            pin = arrow(P3(zx, y + 0.5), P3(zx - 12 * k, y + 0.5), color=MAG, width=7)
            dpa = arrow(P3(zx - 12 * k, y - 0.25), P3(zx + (8 * k if extra else 0), y - 0.25), color=MAG, width=9)
            z = DashedLine(P3(zx, y + 0.95), P3(zx, y - 0.7), color=DIM, stroke_width=2)
            ld = tex(r"\Delta\vec p", MAG, 42).next_to(dpa, DOWN, buff=0.12)
            grp.add(VGroup(r, pin, dpa, z, ld))
        nota = VGroup(tex(r"|\Delta\vec p|:", MAG, 44), tex(r"12\ \to\ 20\ \mathrm{kg\cdot m/s}", MAG, 44)).arrange(RIGHT, buff=0.3).move_to(P3(0, -1.75)).align_to(P3(1.2, 0), LEFT)
        self.play(FadeIn(grp[0][0]), GrowArrow(grp[0][1]), FadeIn(grp[0][3]), run_time=0.6)
        self.play(GrowArrow(grp[0][2]), FadeIn(grp[0][4]), run_time=0.6)
        self.ate(0.35)
        self.play(FadeIn(grp[1][0]), GrowArrow(grp[1][1]), FadeIn(grp[1][3]), run_time=0.6)
        self.play(GrowArrow(grp[1][2]), FadeIn(grp[1][4]), Indicate(a2, color=WHITE_, scale_factor=1.05), run_time=0.6)
        self.ate(0.5)
        self.play(Write(nota), run_time=0.8)
        self.wait(1.0)                                   # G2: a unidade completa fica parada antes da DICA
        self.dica_entra(dica("REBATER PEDE MAIS IMPULSO QUE PARAR"))
        self.ate(0.97)

    # ── E2 ──────────────────────────────────────────────────────────────────────────────────────────────────
    def e2(self):
        self.clear(rt=0.5)
        self.secao("EXERCÍCIO 2 · CHUTE EM 2D", "IMPULSO POR COMPONENTES")
        self.an("E2-1")
        # v6: o esquema já nasce no tamanho final (canto de cima à esquerda); o triângulo do E2-3 tem lugar reservado embaixo
        r1 = txt("ANTES", T_LAB, color=GEO).move_to(P3(-5.6, 1.9))
        r2 = txt("DEPOIS", T_LAB, color=GEO).move_to(P3(-5.6, -0.7))
        b1, a1 = self.bola_vel(-1.2, 1.3, (-2.6, 0))
        b2, a2 = self.bola_vel(-4.6, -2.3, (3.2 * math.cos(PI / 4), 3.2 * math.sin(PI / 4)))
        t1 = tex(r"20\ \mathrm{m/s}", VEL, 40).next_to(a1, UP, buff=0.18)
        t2 = tex(r"30\ \mathrm{m/s}", VEL, 40).next_to(a2.get_end(), RIGHT, buff=0.2)
        arc = Arc(radius=0.9, start_angle=0, angle=PI / 4, arc_center=P3(-4.6, -2.3), color=WHITE_, stroke_width=2)
        a45 = tex(r"45^\circ", WHITE_, 34).move_to(P3(-4.6, -2.3) + P3(1.25, 0.42))
        hor = DashedLine(P3(-4.6, -2.3), P3(-2.9, -2.3), color=DIM, stroke_width=2)
        pe = RoundedRectangle(corner_radius=0.14, width=1.4, height=0.44).set_stroke(GEO, 2).set_fill(STEEL, 1.0) \
            .rotate(-PI / 6).move_to(P3(-5.5, -2.85))
        c = 3.2 * math.cos(PI / 4)
        cx_ = DashedLine(P3(-4.6, -2.3), P3(-4.6 + c, -2.3), color=VEL, stroke_width=3)
        cy_ = DashedLine(P3(-4.6 + c, -2.3), P3(-4.6 + c, -2.3 + c), color=VEL, stroke_width=3)
        lcx = tex(r"21{,}2", VEL, 36).next_to(cx_, DOWN, buff=0.14)
        lcy = tex(r"21{,}2", VEL, 36).next_to(cy_, RIGHT, buff=0.16)
        cena = VGroup(r1, r2, b1, a1, t1, b2, a2, t2, arc, a45, hor, pe, cx_, cy_, lcx, lcy)
        cena.scale(0.8).align_to(P3(-6.6, 0), LEFT).align_to(P3(0, 2.0), UP)
        for m in (t1, t2, a45, lcx, lcy):
            m.scale(1.15)                                       # rótulos ≥ 28 px depois da escala
        d1, d2 = tex(r"m=0{,}40\ \mathrm{kg}", WHITE_, 46), tex(r"\Delta t=0{,}010\ \mathrm{s}", WHITE_, 46)
        conta(d1, d2, topo=2.2, buff=0.35)
        self.play(FadeIn(r1), FadeIn(b1, shift=0.4 * LEFT), GrowArrow(a1), FadeIn(t1), run_time=0.7)      # já entra com a seta
        self.play(Write(d1), Indicate(b1, color=WHITE_, scale_factor=1.25), run_time=0.8)
        self.ate(0.3)
        self.play(FadeIn(pe, shift=0.3 * UR), run_time=0.5)
        self.ate(0.4)
        self.play(FadeIn(r2), FadeIn(b2), run_time=0.5)
        self.play(GrowArrow(a2), FadeIn(t2), run_time=0.7)
        self.ate(0.5)
        self.play(FadeIn(hor), Create(arc), FadeIn(a45), run_time=0.8)
        self.ate(0.55)
        self.play(Indicate(a2, color=WHITE_, scale_factor=1.08), Indicate(a45, color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.ate(0.6)
        self.play(Write(d2), Indicate(pe, color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.ate(0.97)
        # E2-2 · 21,2 acende nos catetos; J_x e J_y nascem dos catetos ------------------------------------------------
        self.an("E2-2")
        vfx = Mc((r"v_{f,x}=v_{f,y}=21{,}2\ \mathrm{m/s}", VEL), size=40)
        jx = Mc((r"J_x", JC), "=", r"0{,}40\,(21{,}2+20)", "=", (r"16{,}5\ \mathrm{N\cdot s}", JC), size=40)
        jy = Mc((r"J_y", JC), "=", r"0{,}40\cdot 21{,}2", "=", (r"8{,}5\ \mathrm{N\cdot s}", JC), size=40)
        conta(d1, d2, vfx, jx, jy, topo=2.2, buff=0.38)
        self.play(FadeOut(hor), FadeOut(arc), FadeOut(a45), Create(cx_), Create(cy_), run_time=0.9)
        self.ate(0.2)
        self.play(Write(vfx), FadeIn(lcx), FadeIn(lcy), run_time=0.9)
        self.ate(0.3)
        self.play(Indicate(lcx, color=WHITE_, scale_factor=1.2), Indicate(lcy, color=WHITE_, scale_factor=1.2), run_time=0.8)
        self.ate(0.42)
        self.play(FadeOut(cx_.copy().set_stroke(JC, 5), target_position=jx[0].get_center(), scale=0.4), Write(jx), Indicate(a1, color=WHITE_), run_time=1.1)
        self.ate(0.62)
        self.play(Indicate(cx_, color=WHITE_), Indicate(jx[4], color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.ate(0.78)
        self.play(FadeOut(cy_.copy().set_stroke(JC, 5), target_position=jy[0].get_center(), scale=0.4), Write(jy), run_time=1.1)
        self.ate(0.9)
        self.play(Indicate(cy_, color=WHITE_), Indicate(jy[4], color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.ate(0.97)
        # E2-3 · triângulo no espaço reservado; F⃗_méd paralela a Δp⃗ e desliza sobre ela ---------------------------------------
        self.an("E2-3")
        self.play(*[FadeOut(m) for m in (vfx, jx, jy, d1, d2)], run_time=0.5)
        s = 0.16
        o = P3(-0.75, -2.35)                                     # origem comum de p_i e p_f
        pi_v, pf_v = np.array([-8.0, 0, 0]) * s, np.array([8.49, 8.49, 0]) * s
        pi_a = arrow(o, o + pi_v, color=MAG, width=7)
        pf_a = arrow(o, o + pf_v, color=MAG, width=7)
        dp_a = arrow(o + pi_v, o + pf_v, color=MAG, width=10, tip=0.26)
        l1 = tex(r"\vec p_i", MAG, 34).next_to(pi_a, DOWN, buff=0.2)
        l2 = tex(r"\vec p_f", MAG, 34).next_to(pf_a.point_from_proportion(0.55), RIGHT, buff=0.25)
        dd = (pf_v - pi_v) / np.linalg.norm(pf_v - pi_v)
        nrm = np.array([-dd[1], dd[0], 0])                    # normal para fora (lado de cima/esquerda)
        l3 = tex(r"\Delta\vec p", MAG, 34).move_to(o + pi_v + (pf_v - pi_v) * 0.42 + nrm * 0.32)
        off = nrm * 0.8
        fmed = arrow(o + pi_v + (pf_v - pi_v) * 0.08 + off, o + pi_v + (pf_v - pi_v) * 0.78 + off, color=FC, width=8, tip=0.24)
        fl = tex(r"\vec F_{\mathrm{m\acute{e}d}}", FC, 34).next_to(fmed.get_end(), UP, buff=0.15)
        res = Mc((r"F_{\mathrm{m\acute{e}d}}", FC), "=", (r"\frac{\Delta p}{\Delta t}", MAG), size=50)
        res2 = Mc((r"1{,}9\times10^{3}\ \mathrm{N}\ \text{a}\ 27^\circ", FC), size=44)
        n1 = Mc((r"\vec F_{\mathrm{m\acute{e}d}}\ \parallel\ \Delta\vec p", FC), size=50)
        n2 = Mc((r"\vec F_{\mathrm{m\acute{e}d}}\ \nparallel\ \vec v_f", FC), size=50)          # não é paralela à velocidade final
        n2[0][-3:].set_color(VEL)
        conta(res, res2, n1, n2, topo=2.0, buff=0.45)
        self.play(GrowArrow(pi_a), GrowArrow(pf_a), Write(res), run_time=0.9)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        self.play(GrowArrow(dp_a), run_time=0.9)
        self.play(FadeIn(l3), run_time=0.4)
        self.ate(0.3)
        self.play(GrowArrow(fmed), FadeIn(fl), Indicate(res, color=WHITE_, scale_factor=1.08), run_time=1.0)
        self.play(Write(res2), run_time=0.8)
        ang_dp = math.degrees(math.atan2(8.49, 16.49))
        arco1 = Arc(radius=0.55, start_angle=0, angle=math.radians(ang_dp), arc_center=o + pi_v, color=WHITE_, stroke_width=2)
        a27 = tex(r"27^\circ", WHITE_, 30).move_to(o + pi_v + P3(0.9, 0.2))
        hor = DashedLine(o + pi_v, o + pi_v + P3(1.3, 0), color=DIM, stroke_width=2)
        arco2 = Arc(radius=0.55, start_angle=0, angle=PI / 4, arc_center=o, color=WHITE_, stroke_width=2)
        a45 = tex(r"45^\circ", WHITE_, 30).move_to(o + P3(0.85, 0.3))
        hor2 = DashedLine(o, o + P3(1.3, 0), color=DIM, stroke_width=2)
        self.ate(0.45)
        self.play(FadeIn(hor2), Create(arco2), FadeIn(a45), run_time=0.9)
        self.ate(0.47)
        self.play(Indicate(VGroup(pi_a, pf_a, dp_a), color=WHITE_, scale_factor=1.04), run_time=0.9)
        self.ate(0.48)
        self.play(Indicate(dp_a, color=WHITE_, scale_factor=1.06), Indicate(l3, color=WHITE_, scale_factor=1.15), run_time=0.9)
        self.ate(0.49)
        self.play(FadeIn(hor), Create(arco1), FadeIn(a27), run_time=0.9)
        # G5: F⃗_méd desliza até ficar sobre Δp⃗ (prova do paralelismo) e volta
        self.ate(0.5)
        self.play(VGroup(fmed, fl).animate.shift(-off), run_time=1.0)
        self.play(Indicate(dp_a, color=WHITE_, scale_factor=1.03), run_time=0.6)
        self.play(VGroup(fmed, fl).animate.shift(off), run_time=0.8)
        self.ate(0.62)
        self.play(Write(n1), run_time=0.8)
        self.ate(0.8)
        self.play(Write(n2), Indicate(a2, color=WHITE_), run_time=0.8)
        self.ate(0.97)
        # E2-4 · DICA -----------------------------------------------------------------------------------------------
        self.an("E2-4")
        self.play(Indicate(dp_a, color=WHITE_), Indicate(fmed, color=WHITE_), run_time=0.6)
        self.dica_entra(dica([MathTex(r"F_{\mathrm{m\acute{e}d}}", font_size=30), "APONTA PARA", MathTex(r"\Delta\vec p", font_size=30), ","],
                             "NÃO PARA A VELOCIDADE FINAL"))
        self.ate(0.97)

    # ── E3 ──────────────────────────────────────────────────────────────────────────────────────────────────
    def e3(self):
        self.clear(rt=0.6)
        self.secao("EXERCÍCIO 3 · FORÇA QUE CRESCE COM O TEMPO", "IMPULSO COMO INTEGRAL")
        self.an("E3-1")
        # v6: foguete numa coluna própria à esquerda, gráfico no meio, conta à direita; o jato cresce com F(t)
        G = Graf(-4.4, -2.8, 4.75, 4.85, 4.0, 8000, MathTex(r"F", font_size=42, color=FC))
        A = 500.0
        fun = lambda t: A * t * t
        curva = G.curva(fun, 0.0, 3.9, n=200)
        tp = ValueTracker(0.0)
        foguete = foguete_t4(0.85).move_to(P3(-5.75, 0.6))
        base = foguete[2].get_bottom()

        def jato():
            f = fun(min(tp.get_value(), 3.9)) / 8000
            L = 0.2 + 2.4 * f
            w = 0.14 + 0.24 * f
            return VGroup(Polygon(base + P3(-w, 0), base + P3(w, 0), base + P3(0, -L)).set_stroke(HEAT, 2).set_fill(HEAT, 0.55),
                          Polygon(base + P3(-w * 0.5, 0), base + P3(w * 0.5, 0), base + P3(0, -L * 0.6)).set_stroke(width=0)
                          .set_fill(mix(HEAT, 0.6), 0.9)).set_z_index(3)
        jt = always_redraw(jato)
        mov = always_redraw(lambda: VGroup(Rectangle(width=0.22, height=max(0.02, G.h * fun(tp.get_value()) / G.fmax)).set_stroke(width=0)
                                           .set_fill(FC, 0.16).move_to((G.pt(tp.get_value(), 0) + G.pt(tp.get_value(), fun(tp.get_value()))) / 2),
                                           DashedLine(G.pt(tp.get_value(), 0), G.pt(tp.get_value(), fun(tp.get_value())), dash_length=0.08)
                                           .set_stroke(WHITE_, 1.6, opacity=0.5),
                                           Dot(G.pt(tp.get_value(), fun(tp.get_value())), radius=0.08, color=WHITE_)).set_z_index(8))
        lab = tex(r"(1{,}25\ \mathrm{s};\ 781{,}25\ \mathrm{N})", WHITE_, 32)
        lab.next_to(G.pt(1.25, fun(1.25)), RIGHT, buff=0.25).shift(DOWN * 0.15)
        msg = tex(r"m=2.150\ \mathrm{kg}", WHITE_, 46)
        aprox = linha(txt("MASSA", 20, color=GEO), MathTex(r"\approx", font_size=30, color=GEO), txt("CONSTANTE (APROXIMAÇÃO)", 20, color=GEO),
                      buff=0.1)                          # v6.1: o foguete real perde massa; aqui é aproximação
        feq = Mc((r"F", FC), "=", "A", (r"t^{2}", WHITE_), size=M_MID)
        aeq = Mc((r"A", WHITE_), "=", r"\frac{781{,}25}{1{,}25^{2}}", "=", r"500\ \mathrm{N/s^{2}}", size=44)
        conta(msg, aprox, feq, aeq, topo=2.2, buff=0.4, x0=1.3)
        aprox.shift(UP * 0.22)
        # sincronia: "no espaço" → estrelas na coluna do foguete (fora do foguete e do eixo do gráfico)
        rng = np.random.default_rng(15)
        estrelas = VGroup(*[Dot(P3(x, y), radius=r, color=WHITE_).set_opacity(o).set_z_index(1) for x, y, r, o in
                            zip(np.r_[rng.uniform(-7.1, -6.6, 6), rng.uniform(-5.05, -4.75, 5)], rng.uniform(-2.9, 2.3, 11),
                                rng.uniform(0.02, 0.045, 11), rng.uniform(0.35, 0.8, 11))])
        self.play(Create(G.eixos), FadeIn(foguete, shift=0.2 * UP), FadeIn(jt), run_time=0.9)
        self.ate(0.08)
        self.play(Write(msg), Indicate(foguete, color=WHITE_, scale_factor=1.06), run_time=0.8)
        self.ate(0.12)
        self.play(LaggedStart(*[FadeIn(e, scale=0.3) for e in estrelas], lag_ratio=0.12), run_time=1.2)
        self.ate(0.16)
        self.add(mov)
        self.play(Create(curva), tp.animate(rate_func=linear).set_value(0.4), run_time=1.6)
        self.ate(0.2)
        self.play(Write(feq), run_time=1.0)
        self.ate(0.25)
        self.play(tp.animate(rate_func=linear).set_value(1.25), run_time=2.4)        # o ponto anda até o dado; o jato cresce junto
        pto = Dot(G.pt(1.25, fun(1.25)), radius=0.09, color=WHITE_).set_z_index(9)
        self.ate(0.3)
        self.play(FadeIn(pto, scale=0.5), FadeIn(lab), run_time=0.7)
        # v6 (G5): o ponto segue pela curva em loop e o jato acompanha F(t) enquanto a fala continua
        t0l = self.clk.get_value()
        tp.add_updater(lambda m: m.set_value(1.25 + 2.65 * (((self.clk.get_value() - t0l) % 4.0) / 4.0)))
        self.add(tp)
        self.ate(0.72)
        self.play(Write(aeq), Indicate(pto, color=WHITE_, scale_factor=1.6), run_time=1.4)
        self.ate(0.86)
        self.play(FadeIn(aprox, shift=0.1 * UP), Indicate(msg, color=WHITE_, scale_factor=1.08), run_time=0.8)
        self.ate(0.97)
        tp.clear_updaters()
        # E3-2 · Riemann e depois a primitiva; o jato segue o cursor entre 2,0 e 3,5 s -------------------------------------
        self.an("E3-2")
        self.play(FadeOut(lab), FadeOut(pto), run_time=0.4)
        t2l = tex(r"2{,}0", DIM, 32).next_to(G.pt(2.0, 0), DOWN, buff=0.12)
        t35 = tex(r"3{,}5", DIM, 32).next_to(G.pt(3.5, 0), DOWN, buff=0.12)
        self.play(FadeIn(t2l), FadeIn(t35), tp.animate.set_value(2.0), run_time=0.5)
        t0c = self.clk.get_value()
        tp.add_updater(lambda m: m.set_value(2.0 + 1.5 * (((self.clk.get_value() - t0c) % 3.0) / 3.0)))
        self.add(tp)

        def ret(n):
            dx = 1.5 / n
            g = VGroup()
            for k in range(n):
                t0 = 2.0 + k * dx
                h = fun(t0 + dx / 2)
                g.add(Rectangle(width=G.w * dx / G.tmax, height=G.h * h / G.fmax).move_to((G.pt(t0, 0) + G.pt(t0 + dx, h)) / 2)
                      .set_stroke(FC, 1.5 if n < 24 else 0.8).set_fill(JC, 0.5).set_z_index(4))
            return g, sum(fun(2.0 + (k + 0.5) * 1.5 / n) * 1.5 / n for k in range(n))
        rr, s3 = ret(3)
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in rr], lag_ratio=0.2), run_time=1.0)
        somas = [s3]
        for n in (6, 24):
            novo, sn = ret(n)
            somas.append(sn)
            self.play(ReplacementTransform(rr, novo), run_time=0.9)
            rr = novo
        print("[QA] E3-2 Riemann (3, 6, 24):", ", ".join(f"{x:.1f}" for x in somas), "N·s (alvo 5812,5)")
        area = G.area(fun, 2.0, 3.5, n=100)
        self.play(FadeTransform(rr, area), run_time=0.8)
        jeq = Mc((r"J", JC), "=", (r"\int_{2{,}0}^{3{,}5}500\,t^{2}\,dt", JC), size=42)
        jeq2 = Mc("=", r"\frac{500}{3}\,(3{,}5^{3}-2{,}0^{3})", size=42)
        res = Mc((r"J\approx5{,}81\times10^{3}\ \mathrm{N\cdot s}", JC), size=44)
        self.play(FadeOut(feq), FadeOut(aeq), run_time=0.4)
        conta(msg, aprox.copy(), jeq, jeq2, res, topo=2.2, buff=0.36, x0=1.3)
        self.play(Write(jeq), Indicate(area, color=WHITE_, scale_factor=1.0), run_time=1.0)
        self.ate(0.65)
        self.play(Write(jeq2), run_time=0.9)
        self.ate(0.85)
        self.play(Write(res), run_time=0.8)
        self.play(Indicate(res, color=WHITE_, scale_factor=1.08), run_time=0.7)
        self.ate(0.97)
        # E3-3 ------------------------------------------------------------------------------------------------
        self.an("E3-3")
        j = area_num(fun, 2.0, 3.5)
        print(f"[QA] E3 J = {j:.2f} N·s (alvo 5812,5); F_med = {j / 1.5:.1f} N; Δv = {j / 2150:.3f} m/s")
        r = G.retangulo(2.0, 3.5, 3875.0)
        dv = Mc((r"\Delta v=\frac{J}{m}=2{,}70\ \mathrm{m/s}", VEL), size=44)
        fm = Mc((r"F_{\mathrm{m\acute{e}d}}=3.875\ \mathrm{N}", FC), size=44)
        pos = alvo_conta(msg, aprox, res, dv, fm, topo=2.2, buff=0.45, x0=1.3)
        dv.move_to(pos[3])
        fm.move_to(pos[4])
        self.play(FadeOut(jeq), FadeOut(jeq2), res.animate.move_to(pos[2]), run_time=0.6)
        self.play(Write(dv), Indicate(foguete, color=WHITE_, scale_factor=1.05), run_time=0.9)
        self.ate(0.55)
        self.play(Create(r), Write(fm), run_time=1.2)
        self.play(Indicate(r, color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.97)
        tp.clear_updaters()
