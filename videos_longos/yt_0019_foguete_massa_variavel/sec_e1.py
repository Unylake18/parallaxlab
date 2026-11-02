"""Lote PE1: E1 — decolagem (2D). ESQUEMA fixo à esquerda: foguete-mestre de pé na mesa de lançamento (sem pernas), piso com grade; os dados nascem
no objeto (m₀ = 20.000 kg com linha-guia no casco, PROPELENTE 16.000 kg no tanque, v_ex = 2.500 m/s no bocal com a seta VREL tracejada, |dm/dt| = 120 kg/s
no jato) e voam para a CONTA. E1-2: setas de empuxo (no bocal) e peso (no CM) em 300 : 196. E1-3: t_q, R = 5, 4.024 − 1.307 = 2.717 m/s e a barra com a perda.
E1-4: zoom na cápsula com o passageiro: a_f = 65,2 m/s² (resultante, ACC) × a_sentida = 75 m/s² (força do assento sobre o passageiro, FC); CONFERE e DICA."""
from pecas19 import *  # noqa: F401,F403

VEX_C = VREL
N_ = lambda s: s.replace(".", "{.}").replace(",", "{,}")


class LoteE1(Prob2):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base()
        self.e1()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def e1(self):
        self.an("E1-1")
        self.secao("EXERCÍCIO 1 · DECOLAGEM")
        XR, YB, H, W = -4.2, -1.7, 4.1, 0.78                              # foguete: x do eixo, y do bocal, altura, largura (mesmas proporções do vertical do T3)
        fg = FogueteMestre(H, W, janela=True).shift(P3(XR, YB))
        Y_PISO = -3.2
        piso = piso_grade(-7.35, 0.2, Y_PISO, prof=0.4)
        mesa = aco(VGroup(*[Rectangle(width=0.1, height=YB - Y_PISO).move_to(P3(XR + s * 0.95, (YB + Y_PISO) / 2)) for s in (-1, 1)]), 1.2)      # dois suportes finos; o piso é uma linha separada
        self.play(FadeIn(piso), FadeIn(mesa), FadeIn(fg), run_time=0.9)
        self.pede("EMPUXO × PESO", x0=-2.0, wmax=9.4)
        g_m0 = Line(P3(XR + 0.42, YB + 0.80 * H), P3(XR + 1.0, YB + 0.80 * H)).set_stroke(GEO, 1.6)
        l_m0 = VGroup(MathTex("m_0=", font_size=40, color=MAS), rot("20.000 kg", 30, MAS)).arrange(RIGHT, buff=0.12).next_to(g_m0.get_end(), RIGHT, buff=0.3)
        g_p = Line(P3(XR + 0.4, YB + 0.42 * H), P3(XR + 1.0, YB + 0.42 * H)).set_stroke(GEO, 1.6)
        l_p = VGroup(txt("PROPELENTE", 24, color=MAS), rot("16.000 kg", 30, MAS)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(g_p.get_end(), RIGHT, buff=0.3)
        ch = chama2d(P3(XR, YB), 0.6, 0.34)
        sx = seta_tr(P3(XR + 1.35, YB - 0.4), P3(XR + 1.35, YB - 1.05), VEX_C, 6, tip=0.2)
        l_vx = VGroup(MathTex(r"v_{ex}=", font_size=40, color=VEX_C), rot("2.500 m/s", 30, VEX_C)).arrange(RIGHT, buff=0.12).next_to(sx, RIGHT, buff=0.2).align_to(sx, UP)
        rel = txt("EM RELAÇÃO AO FOGUETE", 24).next_to(l_vx, DOWN, buff=0.14).align_to(l_vx, LEFT)
        rel.move_to(P3(XR + 1.35 + 0.28 + rel.width / 2, rel.get_center()[1]))          # v6: começa à direita da seta v_ex (a seta não cruza o E)
        l_dm = VGroup(MathTex(r"\left|\frac{dm}{dt}\right|=", font_size=36, color=MAS), rot("120 kg/s", 26, MAS)).arrange(DOWN, buff=0.08, aligned_edge=RIGHT)
        l_dm.move_to(P3(XR - 1.15 - l_dm.width / 2, YB + 0.55))                         # v7 #26: à esquerda da perna da torre, fora dela
        self.gat("um foguete de vinte toneladas")
        self.play(FadeIn(g_m0), FadeIn(l_m0), run_time=0.6)
        self.gat("das quais dezesseis são propelente")
        self.play(FadeIn(g_p), FadeIn(l_p), run_time=0.6)
        self.gat("o gás sai a dois mil e quinhentos")
        self.play(FadeIn(ch), Create(sx), FadeIn(l_vx), FadeIn(rel), run_time=0.8)
        self._refs.append([int(round(self.clk.get_value() * FPS)), "v_ex", "EM RELAÇÃO AO FOGUETE", "rótulo junto da seta"]) if AUDITORIA else None
        self.gat("o motor queima cento e vinte")
        self.play(FadeIn(l_dm), run_time=0.6)
        self.gat("gravidade constante")
        self.hip([["SUBIDA VERTICAL ·", MathTex("g", font_size=32, color=ACC), rot("= 9,8 m/s²", 24), "· SEM AR"]], x0=-2.0, wmax=9.4)
        q = VGroup(txt("DECOLA? COM QUE ACELERAÇÃO?", 26, bold=True), txt("COM QUE VELOCIDADE TERMINA?", 26, bold=True)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(q)
        self.gat("ele decola")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.foco = q
        self.ate(0.97)
        # ── E1-2 ──
        self.an("E1-2")
        self.pilha.limpa(rt=0.3)
        self.play(FadeOut(rel), FadeOut(g_m0), FadeOut(g_p), run_time=0.3)                # v7 #29: as chamadas saem antes das setas de força
        KF = 1.8 / 300.0                                                # setas: 1,8 unidades para 300 kN
        yc_ = YB + H / 2
        DXF = 0.55                                                      # v5: setas fora do casco, uma de cada lado do eixo
        se = arrow(P3(XR - DXF, YB), P3(XR - DXF, YB + KF * 300), FC, 7, tip=0.24)                 # o empuxo nasce no bocal (à esquerda)
        sp = arrow(P3(XR + DXF, yc_), P3(XR + DXF, yc_ - KF * 196), FC, 7, tip=0.24)               # o peso nasce no centro de massa (à direita)
        self.reg("setas_e1", emp=KF * 300, peso=KF * 196, razao=300 / 196)
        self.reg("forca", lugar="E1-2", d_px=0.0, nota="empuxo no bocal (y = YB), peso no CM (y = YB + H/2); deslocamento lateral 14 px (G33 v3)")
        le = MathTex(r"F_{emp}", font_size=40, color=FC).next_to(P3(XR - 0.75, YB + KF * 300 - 0.15), LEFT, buff=0.12)
        lpg = M("m_0", "g", size=40, cores={1: ACC})[0].next_to(P3(XR + 0.8, yc_ - KF * 196 - 0.3), RIGHT, buff=0.12)
        A, ia = M(r"F_{emp}", "=", N_("2.500"), r"\cdot", "120", size=46, cores={0: FC, 2: VEX_C})
        A2, ia2 = M("=", N_(r"300.000\ \mathrm{N}"), size=46, cores={1: FC})
        self.pilha.poe(A)
        self.gat("empuxo: velocidade de exaustão vezes vazão")
        self.play(FadeIn(mp(A, ia, [0, 1, 2, 3, 4])), Indicate(l_vx[1], color=WHITE_, scale_factor=1.06), Indicate(l_dm[1], color=WHITE_, scale_factor=1.06), run_time=0.9)    # v7 #28
        self.gat("trezentos mil newtons")
        self.pilha.poe(A2)
        self.play(FadeIn(A2), GrowArrow(se), FadeIn(le), run_time=0.8)
        B, ib = M("m_0", "g", "=", N_("20.000"), r"\cdot", N_("9,8"), "=", N_(r"196.000\ \mathrm{N}"), size=46, cores={1: ACC, 5: ACC, 7: FC})
        self.pilha.poe(B)
        self.play(GrowArrow(sp), FadeIn(lpg), run_time=0.7)
        self.gat("peso: vinte mil quilos")
        self.play(FadeIn(mp(B, ib, [0, 1, 2, 3, 4, 5])), Indicate(l_m0[1], color=WHITE_, scale_factor=1.06), run_time=0.9)                                              # v7 #28
        self.play(FadeIn(mp(B, ib, [6, 7])), run_time=0.6)
        C = linha_m(M(r"300\ \mathrm{kN}", ">", r"196\ \mathrm{kN}", size=46, cores={0: FC, 2: FC})[0], MathTex(r"\checkmark", font_size=46, color=WHITE_), txt("DECOLA", 28, bold=True), buff=0.2)
        self.pilha.poe(C)
        self.gat("o empuxo ganha")
        self.play(FadeIn(C), run_time=0.7)
        D, id_ = M("a_0", "=", N_(r"\frac{300.000-196.000}{20.000}"), size=46, cores={0: ACC})
        D2, id2 = M("=", N_(r"5,2\ \mathrm{m/s^2}"), size=46, cores={1: ACC})
        self.pilha.poe(D)
        self.pilha.poe(D2)
        self.gat("a aceleração inicial")
        self.play(FadeIn(D), run_time=0.8)
        self.gat("cinco vírgula dois")
        self.play(FadeIn(D2), run_time=0.6)
        self.foco = D
        self.ate(0.97)
        # ── E1-3 ──
        self.an("E1-3")
        self.pilha.limpa(rt=0.3)
        E, ie = M("t_q", "=", N_(r"\frac{16.000}{120}"), r"\approx", r"133\ \mathrm{s}", size=46, cores={0: VEL, 4: VEL})
        self.pilha.poe(E)
        self.gat("agora o tempo de queima")
        self.play(FadeIn(mp(E, ie, [0, 1])), run_time=0.4)                                              # v10 F6: "t_q =" existe antes de o número chegar
        self.acende([(l_p[1][:6], mp(E, ie, [2])[:6]), (l_dm[1][:3], mp(E, ie, [2])[7:])], extra=[FadeIn(mp(E, ie, [2])[6:7])], rt=0.9)
        self.play(FadeIn(mp(E, ie, [3, 4])), run_time=0.5)
        F_, if_ = M("m_f", "=", N_(r"4.000\ \mathrm{kg}"), r"\ \Rightarrow\ ", "R", "=", "5", size=46)
        self.pilha.poe(F_)
        self.gat("a massa final")
        self.play(FadeIn(F_), run_time=0.7)
        G1, ig1 = M(r"v_{ex}\ln 5", r"\approx", N_(r"4.024\ \mathrm{m/s}"), size=46, cores={2: VEL})
        pinta(G1, ig1, 0, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        self.pilha.poe(G1)
        self.gat("no espaço")
        self.play(FadeIn(G1), run_time=0.7)
        G2, ig2 = M(r"g\,t_q", r"\approx", N_(r"1.307\ \mathrm{m/s}"), size=46, cores={2: VEL})
        pinta(G2, ig2, 0, [(0, ACC)])
        self.pilha.poe(G2)
        self.gat("só que aqui a gravidade cobra")
        self.play(FadeIn(G2), run_time=0.7)
        H_, ih = M(r"\Delta v", r"\approx", N_(r"2.717\ \mathrm{m/s}"), size=50, cores={0: VEL, 2: VEL})
        Hb = caixa_l(H_, VEL)
        self.pilha.poe(Hb)
        self.gat("sobram uns dois mil")
        self.play(FadeIn(Hb), run_time=0.7)
        # barra: 4.024 com a perda de 1.307 apagada (laranja: o que vai embora)
        wb = 5.4
        b1 = Rectangle(width=wb * 2717 / 4024, height=0.3).set_stroke(width=0).set_fill(VEL, 0.9)
        b2 = Rectangle(width=wb * 1307 / 4024, height=0.3).set_stroke(HEAT, 2).set_fill(HEAT, 0.25)
        bar = VGroup(b1, b2).arrange(RIGHT, buff=0)
        lperda = txt("PERDA POR GRAVIDADE", 24, color=HEAT)
        gb = VGroup(bar, lperda).arrange(DOWN, buff=0.18, aligned_edge=RIGHT)
        self.pilha.poe(gb)
        self.gat("quase um terço do ganho")
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(lperda), run_time=0.8)
        self.reg("e1_3", perda_frac=1307 / 4024)
        self.foco = gb
        self.ate(0.97)
        # ── E1-4: resultante × sentida (zoom na cápsula, o passageiro DENTRO) ──
        self.an("E1-4")
        self.pilha.limpa(rt=0.3)
        ch_v = chama2d(P3(XR - 2.2, YB), 1.0, 0.4)
        self.play(FadeOut(VGroup(l_m0, g_m0, l_p, g_p, l_dm, l_vx, sx, se, sp, le, lpg, piso, mesa)), fg.animate.shift(2.2 * LEFT), Transform(ch, ch_v), run_time=0.7)      # em voo: sem rampa, jato aceso
        I1, ii1 = M("a_f", "=", N_(r"\frac{300.000-4.000\cdot 9,8}{4.000}"), size=46, cores={0: ACC})
        I1b = linha_m(M(r"\approx", N_(r"65,2\ \mathrm{m/s^2}"), r"\approx", N_("6,7"), "g", size=46, cores={1: ACC, 4: ACC})[0], txt("RESULTANTE", 26, bold=True), buff=0.2)
        self.pilha.poe(I1)
        self.pilha.poe(I1b, dx=0.0)
        self.gat("e no último instante da queima")
        self.play(FadeIn(mp(I1, ii1, [0, 1, 2])), run_time=0.8)
        self.gat("a aceleração resultante vai")
        self.play(FadeIn(I1b), run_time=0.7)
        I2, ii2 = M(r"a_{sentida}", "=", r"\frac{F_{emp}}{m}", "=", N_(r"\frac{300.000}{4.000}"), size=46, cores={0: ACC})
        I2b = VGroup(M("=", r"75\ \mathrm{m/s^2}", r"\approx", N_("7,7"), "g", size=46, cores={1: ACC, 4: ACC})[0], txt("O QUE A CARGA SENTE", 26, bold=True)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        pinta(I2, ii2, 2, [(0, FC), (1, FC), (2, FC), (3, FC)])
        self.pilha.poe(I2)
        self.pilha.poe(I2b, dx=0.3)
        # zoom na cápsula: o passageiro sentado no assento, a força do assento (FC, 75) e a resultante (ACC, 65,2)
        PXc, PYc, PW, PH = -1.9, -0.1, 4.0, 4.0
        jan_c = fg.pts["janela"] + P3(XR - 2.2, YB)
        painel = RoundedRectangle(corner_radius=0.14, width=PW, height=PH).move_to(P3(PXc, PYc)).set_fill("#0A1A38", 0.95).set_stroke("#9AA6B8", 3)
        painel._fundo = True
        guia = VGroup(Line(P3(XR - 2.2 + W / 2, jan_c[1] + 0.35), P3(PXc - PW / 2, PYc + 0.6)).set_stroke(GEO, 1.4, opacity=0.8),
                      Line(P3(XR - 2.2 + W / 2, jan_c[1] - 0.35), P3(PXc - PW / 2, PYc - 1.0)).set_stroke(GEO, 1.4, opacity=0.8))
        y_s = PYc - 1.3
        mq = manequim(PXc + 0.2, y_s, alt=2.6)                               # ~1,5× maior
        assento = aco(Rectangle(width=1.1, height=0.14).move_to(P3(PXc + 0.2, y_s - 0.07)), 1.2)
        K = 2.0 / 75.0
        sF = arrow(P3(PXc - 0.1, y_s), P3(PXc - 0.1, y_s + K * 75), FC, 7, tip=0.22)                  # nasce no assento e atravessa o centro do corpo
        sA = arrow(P3(PXc + 1.5, y_s), P3(PXc + 1.5, y_s + K * 65.2), ACC, 7, tip=0.22)
        self.reg("e1_4", seta_assento=K * 75, seta_res=K * 65.2)
        lF = VGroup(txt("FORÇA DO", 24, color=FC), txt("ASSENTO", 24, color=FC)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        lF.move_to(P3(PXc - PW / 2 + 0.2, y_s + 2.85), aligned_edge=LEFT)
        lF_g = VGroup()
        lA = MathTex("a_f", font_size=38, color=ACC).next_to(sA, UP, buff=0.18)
        self.gat("e o que a carga sente")
        self.play(FadeIn(painel), FadeIn(guia), FadeIn(mq), FadeIn(assento), run_time=0.7)
        self.gat("quem aperta é só o empuxo")
        self.play(GrowArrow(sF), FadeIn(lF), FadeIn(lF_g), GrowArrow(sA), FadeIn(lA), run_time=0.9)
        self.gat("então a carga sente")
        self.play(FadeIn(I2), run_time=0.8)
        self.play(FadeIn(I2b), run_time=0.5)
        self.gat("confere com o que a gente viu")
        self.confere([[MathTex(r"\Delta v", font_size=34, color=VEL), txt("NO ESPAÇO", 24), rot("= 4.024 >", 26), MathTex(r"v_{ex}", font_size=34, color=VEX_C), rot("= 2.500", 26), MathTex(r"\checkmark", font_size=34)]], x0=-2.0, wmax=9.4)
        self.gat("e a dica")
        C2 = linha_m(M(r"300\ \mathrm{kN}", ">", r"196\ \mathrm{kN}", size=46, cores={0: FC, 2: FC})[0], MathTex(r"\checkmark", font_size=46, color=WHITE_), txt("DECOLA", 28, bold=True), buff=0.2)
        self.pilha.poe(C2)                                       # G36: a comparação que a DICA resume volta, compacta, acima dela
        self.play(FadeIn(C2), run_time=0.35)
        self.dica18("COMPARE EMPUXO E PESO")
        self.ate(0.97)
