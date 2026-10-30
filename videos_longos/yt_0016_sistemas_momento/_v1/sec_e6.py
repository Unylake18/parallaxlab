"""Lote Q6: E6 — agarrar ou rebater (Sears, exercício 8.20). Você 70,0 kg no gelo; bola 0,600 kg a 10,0 m/s. Agarra: 0,0850 m/s
(30 J → 0,25 J); rebate a 8,0 m/s: 0,154 m/s (30 J → ≈ 20 J)."""
from kit import *  # noqa: F401,F403

MV, MB, VB, VR = 70.0, 0.600, 10.0, 8.0
V_AG = MB * VB / (MV + MB)
V_RB = MB * (VB + VR) / MV
K0 = MB * VB ** 2 / 2
K_AG = (MV + MB) * V_AG ** 2 / 2
K_RB_B, K_RB_V = MB * VR ** 2 / 2, MV * V_RB ** 2 / 2
assert abs(V_AG - 0.0850) < 1e-4 and abs(V_RB - 0.1543) < 1e-4 and K0 == 30.0 and abs(K_AG - 0.255) < 1e-3
assert abs(K_RB_B - 19.2) < 1e-9 and abs(K_RB_V - 0.833) < 1e-3 and abs(K_RB_B + K_RB_V - 20.03) < 0.01
Y_G = -1.3
XR = 3.9
XP = -2.0                     # posição dos pés


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


class LoteE6(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 6 · AGARRAR OU REBATER", selo="SEARS · EX. 8.20")
        self.e6_1()
        self.e6_2()
        self.e6_3()
        self.e6_4()
        self.fim()
        self.relatorio()

    def cena(self):
        self.gl = gelo(-7.3, 0.6, Y_G)
        self.pessoa = PessoaPerfil(XP, Y_G, 2.0, -1, "pe")
        self.mao = PessoaPerfil(XP, Y_G, 2.0, -1, "agarra").pts["mao_f"]
        self.fr = fronteira(7.0, 2.95, P3(-3.55, Y_G + 1.25), rotulo=["VOCÊ", mais(), "A BOLA"])

    def e6_1(self):
        self.an("E6-1")
        self.cena()
        bl = bola(0.17).move_to(P3(-6.6, self.mao[1]))
        va = arrow(P3(-6.35, self.mao[1] + 0.45), P3(-5.0, self.mao[1] + 0.45), color=VEL, width=6, tip=0.17)
        lv = num(r"10{,}0\ \mathrm{m/s}", VEL, 30).next_to(va, UP, buff=0.1)
        dados = VGroup(num(r"m_{\text{você}}=70{,}0\ \mathrm{kg}"), num(r"m_{\text{bola}}=0{,}600\ \mathrm{kg}")) \
            .arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(P3(XR, 1.55))
        self.play(FadeIn(self.gl), FadeIn(self.pessoa), run_time=0.8)
        self.play(FadeIn(bl), GrowArrow(va), FadeIn(lv), FadeIn(dados), run_time=0.9)
        self.ate(0.6)
        self.play(Create(self.fr[0]), FadeIn(self.fr[1]), run_time=1.0)
        sh = txt("NA HORIZONTAL: SEM FORÇA EXTERNA", 20, color=FC).move_to(P3(XR, 0.25))
        self.play(FadeIn(sh), run_time=0.6)
        self.ate(0.97)
        self.bl, self.va, self.lv, self.dados, self.sh = bl, va, lv, dados, sh

    def e6_2(self):
        self.an("E6-2")
        t1 = txt("AGARRA", T_MAIN, bold=True).move_to(P3(XR, 0.35))
        e1 = num(r"V=\frac{0{,}600\cdot 10{,}0}{70{,}6}=0{,}085\ \mathrm{m/s}", VEL, 40).move_to(P3(XR, -1.45))
        en = Mc((r"K:\ 30\ \mathrm{J}\ \to\ 0{,}25\ \mathrm{J}", KC), size=38).move_to(P3(XR, -2.45))
        self.play(FadeOut(self.sh), FadeIn(t1), run_time=0.5)
        nova = PessoaPerfil(XP, Y_G, 2.0, -1, "agarra")
        self.play(FadeOut(self.va), FadeOut(self.lv), Transform(self.pessoa, nova), self.bl.animate.move_to(self.mao + P3(-0.12, 0.02)),
                  run_time=1.2, rate_func=linear)
        pm = num(r"p=0{,}600\cdot 10{,}0=6{,}0\ \mathrm{kg\cdot m/s}", MAG, 34).move_to(P3(XR, -0.4))
        self.play(FadeIn(pm), run_time=0.6)
        self.ate(0.4)
        grupo = VGroup(self.pessoa, self.bl)
        vV = arrow(P3(XP - 0.4, Y_G + 2.35), P3(XP + 0.6, Y_G + 2.35), color=VEL, width=6, tip=0.17)
        lV = num(r"V", VEL, 40).next_to(vV, RIGHT, buff=0.12)
        self.play(grupo.animate.shift(RIGHT * 0.35), GrowArrow(vV), FadeIn(lV), FadeIn(e1, shift=0.1 * UP), run_time=1.6, rate_func=linear)
        self.ate(0.75)
        self.play(FadeIn(en, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        self.lixo = VGroup(t1, e1, en, vV, lV, pm)

    def e6_3(self):
        self.an("E6-3")
        self.play(FadeOut(self.lixo), FadeOut(self.pessoa), FadeOut(self.bl), run_time=0.5)
        self.pessoa = PessoaPerfil(XP, Y_G, 2.0, -1, "pe")
        bl = bola(0.17).move_to(P3(-6.6, self.mao[1]))
        t2 = txt("REBATE", T_MAIN, bold=True).move_to(P3(XR, 0.25))
        self.play(FadeIn(self.pessoa), FadeIn(bl), FadeIn(t2), run_time=0.6)
        peito = self.pessoa.pts["peito"]
        self.play(bl.animate.move_to(P3(peito[0] - 0.3, self.mao[1])), run_time=1.0, rate_func=linear)
        vb = arrow(P3(peito[0] - 0.6, self.mao[1] + 0.45), P3(peito[0] - 1.7, self.mao[1] + 0.45), color=VEL, width=6, tip=0.17)
        lvb = num(r"8{,}0\ \mathrm{m/s}", VEL, 30).next_to(vb, UP, buff=0.1)
        vV = arrow(P3(XP - 0.4, Y_G + 2.35), P3(XP + 0.75, Y_G + 2.35), color=VEL, width=6, tip=0.17)
        lV = num(r"V", VEL, 40).next_to(vV, RIGHT, buff=0.12)
        self.play(bl.animate.shift(LEFT * 2.4), self.pessoa.animate.shift(RIGHT * 0.6), GrowArrow(vb), FadeIn(lvb), GrowArrow(vV), FadeIn(lV),
                  run_time=1.6, rate_func=linear)
        e2 = num(r"70{,}0\,V=0{,}600\,(10{,}0+8{,}0)", WHITE_, 40).move_to(P3(XR, -0.6))
        e3 = num(r"V=0{,}154\ \mathrm{m/s}", VEL, 44).move_to(P3(XR, -1.45))
        en = Mc((r"K:\ 30\ \mathrm{J}\ \to\ 20\ \mathrm{J}", KC), size=38).move_to(P3(XR, -2.3))
        self.ate(0.3)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.45)
        self.play(FadeIn(e3, shift=0.1 * UP), run_time=0.7)
        dobro = txt("QUASE O DOBRO", 18, color=DIM).next_to(e3, RIGHT, buff=0.25)
        self.play(FadeIn(dobro), FadeIn(en), run_time=0.6)
        # miniatura do vídeo anterior (E1: parar × rebater): o Δp de rebater é maior
        self.ate(0.68)
        k = 0.12
        o = P3(-4.3, -2.65)
        mini = VGroup(placa(4.3, 1.35, o + P3(0.55, -0.32), op=0.04))
        da = arrow(o + P3(0.6, 0), o + P3(0.6 - 10 * k, 0), color=MAG, width=5, tip=0.13)
        db = arrow(o + P3(0.6, -0.55), o + P3(0.6 - 18 * k, -0.55), color=MAG, width=5, tip=0.13)
        mini.add(da, db, txt("PARAR", 16, color=DIM).next_to(da, RIGHT, buff=0.2), txt("REBATER", 16, color=DIM).next_to(db, RIGHT, buff=0.2))
        mini.add(tex(r"\Delta\vec p", MAG, 26).next_to(da, LEFT, buff=0.1).shift(0.05 * UP))
        mini.add(txt("VÍDEO ANTERIOR", 14, color=DIM, op=0.8).move_to(o + P3(0.55, 0.55)))
        self.play(FadeIn(mini), run_time=0.7)
        self.ate(0.97)

    def e6_4(self):
        self.an("E6-4")
        self.clear(rt=0.6)
        S = 0.063                                     # u por joule
        yb = -2.65
        cols = {}
        for nome, xc, depois, calor, setas in (
                ("AGARRAR", -5.3, K_AG, K0 - K_AG, ((MB * VB, None),)),
                ("REBATER", -1.0, K_RB_B + K_RB_V, K0 - K_RB_B - K_RB_V, ((MV * V_RB, -MB * VR),))):
            g = VGroup(txt(nome, 26, bold=True).move_to(P3(xc, 2.0)))
            # momento antes/depois (magenta), escala 0,2 u por kg·m/s
            k = 0.2
            o = P3(xc - 0.4, 1.3)
            g.add(txt("ANTES", 14, color=DIM).move_to(o + P3(-1.15, 0)), arrow(o, o + P3(6.0 * k, 0), color=MAG, width=6, tip=0.15))
            o2 = P3(xc - 0.4, 0.75)
            g.add(txt("DEPOIS", 14, color=DIM).move_to(o2 + P3(-1.15, 0)))
            pv, pb = setas[0]
            if pb is None:
                g.add(arrow(o2, o2 + P3(pv * k, 0), color=MAG, width=6, tip=0.15))
            else:
                g.add(arrow(o2, o2 + P3(pv * k, 0), color=MAG, width=6, tip=0.15),
                      arrow(o2 + P3(0, -0.22), o2 + P3(pb * k, -0.22), color=MAG, width=6, tip=0.15))
            g.add(num(r"6{,}0", MAG, 24).next_to(o + P3(6.0 * k, 0), RIGHT, buff=0.12))
            # energia: antes (ciano) × depois (ciano + laranja)
            ba = Rectangle(width=0.7, height=K0 * S).set_stroke(width=0).set_fill(KC, 0.8).move_to(P3(xc - 0.75, yb + K0 * S / 2))
            bd = Rectangle(width=0.7, height=max(depois * S, 0.025)).set_stroke(width=0).set_fill(KC, 0.8) \
                .move_to(P3(xc + 0.75, yb + max(depois * S, 0.025) / 2))
            bc = Rectangle(width=0.7, height=calor * S).set_stroke(mix(HEAT, 0.3), 1.5).set_fill(HEAT, 0.55) \
                .move_to(P3(xc + 0.75, yb + depois * S + calor * S / 2))
            g.add(Line(P3(xc - 1.4, yb), P3(xc + 1.4, yb)).set_stroke(DIM, 2), ba, bd)
            g.add(num(r"30\ \mathrm{J}", KC, 26).next_to(ba, UP, buff=0.08))
            g.add(txt("ANTES", 14, color=DIM).next_to(ba, DOWN, buff=0.1), txt("DEPOIS", 14, color=DIM).next_to(bd, DOWN, buff=0.1))
            cols[nome] = (g, bc, bd, depois, calor)
        ag, rb = cols["AGARRAR"], cols["REBATER"]
        self.play(FadeIn(ag[0]), run_time=0.9)
        self.ate(0.18)
        self.play(FadeIn(ag[1]), FadeIn(num(r"0{,}25\ \mathrm{J}", KC, 24).next_to(ag[2], RIGHT, buff=0.1)), run_time=0.8)
        lc = num(r"\approx 29{,}7\ \mathrm{J}", HEAT, 24).next_to(ag[1], RIGHT, buff=0.1)
        cl = VGroup(Square(0.16).set_stroke(width=0).set_fill(HEAT, 0.6), txt("CALOR E DEFORMAÇÃO", 14, color=HEAT)).arrange(RIGHT, buff=0.12).move_to(P3(-3.15, -3.55))
        un = num(r"\mathrm{kg\cdot m/s}", MAG, 22).move_to(P3(-3.15, 1.6))
        self.play(FadeIn(lc), FadeIn(cl), FadeIn(un), run_time=0.6)
        self.ate(0.4)
        self.play(FadeIn(rb[0]), run_time=0.8)
        self.play(FadeIn(rb[1]), FadeIn(num(r"\approx 20\ \mathrm{J}", KC, 24).next_to(rb[2], RIGHT, buff=0.1)),
                  FadeIn(num(r"\approx 10\ \mathrm{J}", HEAT, 24).next_to(rb[1], RIGHT, buff=0.1)), run_time=0.8)
        m1 = txt("MOMENTO: CONSERVADO NOS DOIS", 24, bold=True, color=MAG).move_to(P3(XR, 1.3))
        m2 = txt("ENERGIA: EM NENHUM", 24, bold=True, color=KC).move_to(P3(XR, 0.65))
        m3 = txt("SÓ SE CONSERVA SE A COLISÃO FOR ELÁSTICA", 16, color=DIM).move_to(P3(XR, 0.1))
        self.ate(0.6)
        self.play(FadeIn(m1, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(m2, shift=0.1 * UP), run_time=0.6)
        self.ate(0.8)
        self.play(FadeIn(m3), run_time=0.5)
        d = dica(["NO MOMENTO O SISTEMA É VOCÊ", mais(30), "A BOLA."], "REBATER TRANSFERE MAIS QUE AGARRAR")
        self.dica_entra(d)
        self.ate(0.97)
        self.dica_sai()
        self.clear(rt=0.5)
