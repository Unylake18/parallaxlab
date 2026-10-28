"""Lote Q8: E8 — os gases do rifle (Sears, exercício 8.17). Bala 7,20 g a 601 m/s em relação ao cano; rifle 2,80 kg recua a 1,85 m/s
em relação ao chão: v_bala = 599,15 m/s; p_bala = 4,31, p_rifle = −5,18, p_gases = +0,866 kg·m/s; sistema = bala + rifle + gases."""
from kit import *  # noqa: F401,F403

MB, MR, VREL, VR = 0.00720, 2.80, 601.0, 1.85
VB = VREL - VR
PB, PR = MB * VB, -MR * VR
PG = -(PB + PR)
assert abs(VB - 599.15) < 1e-9 and abs(PB - 4.314) < 1e-3 and abs(PR + 5.18) < 1e-9 and abs(PG - 0.866) < 1e-3
XR = 3.9
YR = 0.6                       # altura do cano
K = 0.6                        # u por kg·m/s no diagrama


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


class LoteE8(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 8 · OS GASES DO RIFLE", selo="SEARS · EX. 8.17")
        self.e8_1()
        self.e8_2()
        self.e8_3_4()
        self.fim()
        self.relatorio()

    def e8_1(self):
        self.an("E8-1")
        rf, boca = rifle(0.0, comp=1.75)
        rf.scale(1.9, about_point=ORIGIN)
        boca = boca * 1.9
        o = P3(-6.6, YR)
        rf.shift(o)
        self.boca = boca + o
        apoio = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.06, width=0.5, height=0.14).set_stroke(width=0).set_fill(TERRA, 1)
                                .move_to(P3(x, YR - 0.33)),
                                Rectangle(width=0.1, height=1.2).set_stroke(width=0).set_fill(TERRA, 1).move_to(P3(x, YR - 0.98)))
                         for x in (-5.9, -4.0)])
        piso = chao(-7.3, -1.5, YR - 1.58)
        la = txt("APOIO FROUXO", 14, color=DIM).move_to(P3(-4.95, YR - 1.85))
        self.play(FadeIn(piso), FadeIn(apoio), FadeIn(la), FadeIn(rf), run_time=0.9)
        self.rf = rf
        dados = VGroup(num(r"m_{\text{rifle}}=2{,}80\ \mathrm{kg}"), num(r"m_{\text{bala}}=7{,}20\ \mathrm{g}")) \
            .arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(P3(XR, 1.75))
        self.play(FadeIn(dados), run_time=0.7)
        self.ate(0.18)
        bl = bala_mob().scale(1.3).move_to(self.boca)
        self.add(bl)
        self.play(bl.animate.shift(RIGHT * 2.2), self.rf.animate.shift(LEFT * 0.25), run_time=0.5, rate_func=linear)
        vb = arrow(self.boca + P3(0.1, 0.85), self.boca + P3(1.9, 0.85), color=VEL, width=6, tip=0.17)
        lb = num(r"601\ \mathrm{m/s}", VEL, 32).next_to(vb, UP, buff=0.08)
        rb = txt("EM RELAÇÃO AO CANO", 15, color=VEL).next_to(lb, UP, buff=0.06)
        vr = arrow(P3(-5.3, YR + 0.6), P3(-6.4, YR + 0.6), color=VEL, width=6, tip=0.17)
        lr = num(r"1{,}85\ \mathrm{m/s}", VEL, 30).next_to(vr, UP, buff=0.08)
        rr = txt("EM RELAÇÃO AO CHÃO", 15, color=VEL).next_to(lr, UP, buff=0.06)
        self.ate(0.3)
        self.play(GrowArrow(vb), FadeIn(lb), FadeIn(rb), run_time=0.8)
        self.ate(0.55)
        self.play(GrowArrow(vr), FadeIn(lr), FadeIn(rr), run_time=0.8)
        pg = txt("OS GASES CARREGAM MOMENTO?", 22).move_to(P3(XR, 0.3))
        self.ate(0.8)
        self.play(FadeIn(pg), run_time=0.6)
        self.ate(0.97)
        self.bl, self.dados, self.pg = bl, dados, pg
        self.setas = VGroup(vb, lb, rb, vr, lr, rr)

    def e8_2(self):
        self.an("E8-2")
        self.play(FadeOut(self.pg), FadeOut(self.dados), run_time=0.4)
        e1 = Mc((r"v_{\text{bala,chão}}", VEL), "=", "601", "-", (r"1{,}85", VEL), "=", (r"599{,}15\ \mathrm{m/s}", VEL), size=44).move_to(P3(XR, 1.85))
        n1 = txt("O CANO ANDA PARA TRÁS", 16, color=DIM).next_to(e1, DOWN, buff=0.16)
        self.play(FadeIn(e1[:3], shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(e1[3:5], shift=0.1 * UP), FadeIn(n1), run_time=0.7)
        self.play(Indicate(e1[4], color=VEL), run_time=0.7)
        self.play(FadeIn(e1[5:]), run_time=0.6)
        # diagrama do momento, ponta com cauda: bala (+4,31) e rifle (−5,18) não fecham
        self.O = O = P3(1.6, -0.6)
        ref = DashedLine(O + P3(0, 0.5), O + P3(0, -2.3), dash_length=0.07).set_stroke(DIM, 1.5, opacity=0.7)
        l0 = num(r"0", DIM, 26).next_to(ref, UP, buff=0.05)
        ab = arrow(O, O + P3(PB * K, 0), color=MAG, width=7, tip=0.2, z=10)
        lab = num(r"p_{\text{bala}}=+4{,}31", MAG, 30).next_to(ab, UP, buff=0.08)
        ar = arrow(O + P3(PB * K, -0.55), O + P3((PB + PR) * K, -0.55), color=MAG, width=7, tip=0.2, z=10)
        lar = num(r"p_{\text{rifle}}=-5{,}18", MAG, 30).next_to(ar, DOWN, buff=0.08)
        un = num(r"\mathrm{kg\cdot m/s}", MAG, 26).move_to(O + P3(4.3, 0.3))
        self.ate(0.5)
        self.play(FadeIn(ref), FadeIn(l0), GrowArrow(ab), FadeIn(lab), FadeIn(un), run_time=0.9)
        self.ate(0.75)
        self.play(GrowArrow(ar), FadeIn(lar), run_time=0.9)
        self.ate(0.97)
        self.diag = VGroup(ref, l0, ab, lab, ar, lar, un)
        self.e1, self.n1 = e1, n1

    def e8_3_4(self):
        self.an("E8-3")
        O = self.O
        fx = (PB + PR) * K
        gap = Line(O + P3(fx, -1.0), O + P3(0, -1.0)).set_stroke(APAGADO, 4)
        nf = txt("NÃO FECHA", 16, color=APAGADO).next_to(gap, LEFT, buff=0.15)
        self.play(Create(gap), FadeIn(nf), run_time=0.7)
        self.ate(0.3)
        # nuvem de gases saindo da boca do cano (partículas translúcidas), com a seta que fecha a soma
        t0 = self.clk.get_value()
        rng = np.random.default_rng(7)
        semente = [(rng.uniform(0.2, 1.0), rng.uniform(-0.5, 0.5), rng.uniform(0.12, 0.3)) for _ in range(16)]
        boca = self.boca + P3(-0.25, 0)

        def nuvem():
            s = min(1.0, (self.clk.get_value() - t0) / 1.4)
            g = VGroup()
            for dx, dy, r in semente:
                c = boca + P3(0.15 + 1.1 * dx * s, dy * s * 0.6)
                g.add(Circle(radius=r * (0.45 + 0.6 * s)).move_to(c).set_stroke(WHITE_, 1.2, opacity=0.35).set_fill(WHITE_, 0.1))
            return g.set_z_index(3)
        nv = always_redraw(nuvem)
        self.add(nv)
        self.wait(1.4)
        nv.clear_updaters()
        pgv = arrow(boca + P3(0.5, -0.85), boca + P3(0.5 + PG * K * 1.6, -0.85), color=MAG, width=6, tip=0.16, z=10)
        lgv = txt("GASES", 16, color=DIM).next_to(pgv, DOWN, buff=0.08)
        ag = arrow(O + P3(fx, -1.0), O + P3(0, -1.0), color=MAG, width=7, tip=0.17, z=11)
        lag = num(r"p_{\text{gases}}=+0{,}866", MAG, 30).next_to(ag, DOWN, buff=0.1).shift(RIGHT * 0.6)
        self.play(FadeOut(gap), FadeOut(nf), GrowArrow(pgv), FadeIn(lgv), GrowArrow(ag), FadeIn(lag), run_time=0.9)
        zero = Mc((r"\sum p", MAG), "=", "0", size=46).move_to(P3(5.6, -1.6))
        self.ate(0.75)
        self.play(FadeIn(zero, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # E8-4 -----------------------------------------------------------------------------------------------
        self.an("E8-4")
        fr = fronteira(6.6, 3.3, P3(-3.75, YR + 0.5), rotulo=None)
        sis = linha("SISTEMA", mais(36, "="), "BALA", mais(36), "RIFLE", mais(36), "GASES", size=28, buff=0.16).move_to(P3(-3.5, -2.5))
        self.play(Create(fr[0]), run_time=0.9)
        self.play(FadeIn(sis, shift=0.1 * UP), run_time=0.7)
        self.ate(0.4)
        d = dica("VELOCIDADE EM RELAÇÃO AO CANO", "NÃO É EM RELAÇÃO AO CHÃO.", "A CONTA FECHA COM OS GASES")
        self.play(FadeOut(zero), run_time=0.3)
        self.dica_entra(d)
        self.ate(0.97)
        self.dica_sai()
        self.clear(rt=0.5)
