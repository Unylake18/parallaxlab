"""Lote PS: S1 (três cartões PANEL, bordas rosa / ciano / GEO), S2 (Three.js 'bastao': os dois bastões do hook parados, a parte grossa sublinhada a
0,63 m e a 0,21 m do eixo; barras 14,1 J e 7,06 J), EN1 (encerramento padrão: logo com anéis violeta, INSCREVA-SE) e EN2 (desafio na rampa:
cilindro maciço × cilindro oco de parede fina, parados juntos no topo). Sem prévia de próximo vídeo."""
from pecas21 import *  # noqa: F401,F403
from sec_hook import KH, PL, PR, RS, YB, HB


def cartao_(conteudo, cor, w=6.4):
    bx = RoundedRectangle(corner_radius=0.14, width=max(w, conteudo.width + 0.6), height=conteudo.height + 0.5).move_to(conteudo).set_fill(PANEL, 0.85).set_stroke(cor, 2.8)
    bx._fundo = bx._caixa = True
    return VGroup(bx, conteudo).set_z_index(20)


class LoteFim(Lote21):
    def corpo(self):
        self.an("S1")
        self.secao("SÍNTESE")
        c1 = cartao_(VGroup(MathTex(r"I=\sum m r^2=\int r^2\,dm", font_size=54), txt("MOMENTO DE INÉRCIA DEPENDE DO EIXO", 26)).arrange(DOWN, buff=0.18), MAS)
        tinge(c1[1][0])
        c2 = cartao_(MathTex(r"K=\tfrac{1}{2}I\omega^2", font_size=60), KC)
        tinge(c2[1])
        c3 = cartao_(VGroup(MathTex(r"I=I_{cm}+Md^2", font_size=50), VGroup(MathTex(r"I_z=I_x+I_y", font_size=50), txt("(PLACAS)", 26)).arrange(RIGHT, buff=0.2))
                     .arrange(DOWN, buff=0.18), GEO)
        tinge(c3[1][0])
        tinge(c3[1][1][0])
        cs = VGroup(c1, c2, c3).arrange(DOWN, buff=0.28).move_to(P3(1.6, -0.45))
        # palco: o disco de pedaços girando devagar (a síntese nunca é só álgebra)
        t0 = self.clk.get_value()
        CD = P3(-5.2, -0.45)
        dv = vivo(lambda: VGroup(DiscoPedacos(CD, 1.55, 4, 10).rotate(0.3 * (self.clk.get_value() - t0), about_point=CD), eixo_cruz(CD, 0.14)))
        self.play(FadeIn(dv), run_time=0.6)
        for c_, fr in zip(cs, ("um o momento de inércia", "dois a energia cinética", "três dois atalhos")):
            self.gat(fr)
            self.play(FadeIn(c_, shift=0.12 * UP), run_time=0.7)
            self.foco = c_
        self.ate(0.99)
        # ── S2: a resposta do começo (Three.js 'bastao'; v3: bastões grandes, um sobre o outro) ──
        self.an("S2")
        self.secao("A RESPOSTA DO COMEÇO")
        KS = 4.8
        cam = cam_b(K=KS)
        P1, P2 = P3(-6.0, 1.45), P3(-2.0, -0.95)                         # pinos: cabo (em cima) e ponta grossa (embaixo), na tela
        (x1, y1), (x2, y2) = (P1[0] / KS, P1[1] / KS), (P2[0] / KS, P2[1] / KS)
        t_s2 = self.clk.get_value()                                     # o balanço parte de zero (o registro do alinhamento 3D × Manim vê o bastão em repouso)
        amp = ValueTracker(1.0)                                         # v9: os bastões balançam de leve nos 1ºs segundos (a tela não fica parada); o balanço cessa quando os CMs aparecem
        self.add(amp)
        def est_s2(t):
            a_ = amp.get_value() * 0.07 * math.sin(2.4 * (t - t_s2))
            if not PEDIDOS3D:                                           # v9: o registro do alinhamento 3D × Manim acompanha o balanço (CMs na posição real a cada quadro)
                self.reg("al_s2", pino0=tela_b(x1, y1, cam), pino1=tela_b(x2, y2, cam),
                         cm0=tela_b(x1 + 0.63 * math.cos(a_), y1 + 0.63 * math.sin(a_), cam), cm1=tela_b(x2 - 0.21 * math.cos(a_), y2 - 0.21 * math.sin(a_), cam))
            return r4({"bs": [{"x": x1, "y": y1, "ang": a_, "piv": 0, "tint": [0, 0.8]},
                              {"x": x2, "y": y2, "ang": PI + a_, "piv": 1, "tint": [0, 0.8]}], "cam": cam})
        f3 = Fundo3D(self, "bastao", est_s2, op=0.0)
        self.add(f3)
        dv.clear_updaters()
        XB1, XB2, YBS = 0.4, 2.4, -3.0
        sob = ValueTracker(1.0)                                         # barras de energia: voltam a subir em "o dobro" (S2)
        self.add(sob)
        bars = vivo(lambda: VGroup(barra_E(XB1, YBS, 3.0 * sob.get_value(), 0.4, hmax=3.0), barra_E(XB2, YBS, 3.0 * NUM["K_grossa"] / NUM["K_cabo"] * sob.get_value(), 0.4, hmax=3.0)))
        nK = VGroup(nm(r"14{,}1\ \mathrm{J}", KC, 40).move_to(P3(XB1, YBS + 3.0 + 0.5)), nm(r"7{,}06\ \mathrm{J}", KC, 40).move_to(P3(XB2, YBS + 3.0 + 0.5)))
        lbS = VGroup(txt("CABO", 24).move_to(P3(XB1, YBS - 0.35)), txt("GROSSA", 24).move_to(P3(XB2, YBS - 0.35)))
        self.troca([dv, *cs], f3.op.animate.set_value(1.0), FadeIn(bars), FadeIn(nK), FadeIn(lbS), seq=True)
        Pt1 = lambda s_: tela_b(x1 + s_, y1, cam)
        Pt2 = lambda s_: tela_b(x2 - s_, y2, cam)
        sub = VGroup(Line(Pt1(0.42) + 0.62 * DOWN, Pt1(0.84) + 0.62 * DOWN).set_stroke(MAS, 7), Line(Pt2(0.42) + 0.62 * DOWN, Pt2(0.0) + 0.62 * DOWN).set_stroke(MAS, 7))
        cms = VGroup(cm_pt(Pt1(0.63), 0.1), cm_pt(Pt2(0.21), 0.1))
        d1 = VGroup(Line(P1 + 0.9 * UP, Pt1(0.63) + 0.9 * UP).set_stroke(GEO, 6), Dot(P1 + 0.9 * UP, radius=0.07, color=GEO), Dot(Pt1(0.63) + 0.9 * UP, radius=0.07, color=GEO))
        d2 = VGroup(Line(P2 + 0.9 * UP, Pt2(0.21) + 0.9 * UP).set_stroke(GEO, 6), Dot(P2 + 0.9 * UP, radius=0.07, color=GEO), Dot(Pt2(0.21) + 0.9 * UP, radius=0.07, color=GEO))
        l1 = nm(r"0{,}63\ \mathrm{m}", GEO, 38).move_to((P1 + Pt1(0.63)) / 2 + 1.35 * UP)
        l2 = nm(r"0{,}21\ \mathrm{m}", GEO, 38).move_to((P2 + Pt2(0.21)) / 2 + 1.35 * UP)
        self.gat("a parte grossa concentra a maior parte da massa")
        self.play(Create(sub), FadeIn(cms), amp.animate.set_value(0.0), run_time=0.8)
        self.gat("com o eixo no cabo")
        self.play(Create(d1), FadeIn(l1), run_time=0.7)
        self.gat("com o eixo na ponta grossa")
        self.play(Create(d2), FadeIn(l2), run_time=0.7)
        k_ = 2.2                                                        # lado do quadrado: d × 2,2 u por metro → áreas na razão 9
        sqA = Square(side_length=0.63 * k_).move_to(P3(5.0, 1.45)).set_fill(MAS, 0.6).set_stroke(MAS, 3).set_z_index(5)
        sqB = Square(side_length=0.21 * k_).move_to(P3(5.0, -0.95)).set_fill(MAS, 0.6).set_stroke(MAS, 3).set_z_index(5)
        lqA = nm(r"0{,}63^2", GEO, 38).next_to(sqA, RIGHT, buff=0.3)
        lqB = nm(r"0{,}21^2", GEO, 38).next_to(sqB, RIGHT, buff=0.3)
        d9 = MathTex(r"\div 9", font_size=54, color=WHITE_).move_to(P3(5.0, 0.2))
        cab = txt("kg·m²  ·  EIXO NO CABO → NA PONTA GROSSA", 24, color=DIM).move_to(P3(1.3, 3.0))
        rg_ = T(r"I_{grossa}:\ 0{,}2676\to 0{,}0382", 38).move_to(P3(1.3, 2.5))
        rc_ = T(r"I_{cabo}:\ 0{,}0147\to 0{,}1029", 38).move_to(P3(1.3, 2.0))
        rs_ = T(r"I:\ 0{,}282\to 0{,}141", 42).move_to(P3(1.3, 1.4))
        self.gat("o termo de eixos paralelos dela")
        self.play(FadeIn(sqA), FadeIn(lqA), FadeIn(cab), FadeIn(rg_), run_time=0.7)
        self.gat("cai nove vezes")
        self.play(FadeIn(sqB), FadeIn(lqB), FadeIn(d9), run_time=0.7)
        self.gat("o cabo faz o contrário")
        self.play(FadeIn(rc_), run_time=0.5)
        self.play(Indicate(rc_, color=WHITE_, scale_factor=1.06), run_time=0.5)       # v10 B5: FadeIn e Indicate no mesmo play deixavam a linha invisível
        self.gat("muda por um fator dois")
        self.play(FadeIn(rs_), run_time=0.6)
        self.play(Indicate(rs_, color=WHITE_, scale_factor=1.06), run_time=0.6)
        self.gat("o dobro da energia")
        self.play(*[self.ind_copia(m, KC, 1.15, 0.8) for m in nK], run_time=0.8)
        R_ = d9
        self.foco = R_
        self.ate(0.99)
        # ── EN1 ──
        self.an("EN1")
        velhos = self.snap()
        self.play(*[m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in velhos if not isinstance(m, ValueTracker)], run_time=0.5)
        for m in velhos:
            m.clear_updaters()
        self.remove(*velhos)
        self.secao(None)
        logo = self.logo(5.4).move_to(P3(0, 1.0))
        aneis = VGroup(*[Circle(radius=r).move_to(P3(0, 1.0)).set_stroke(VEL, 2.4, opacity=o) for r, o in ((2.2, 0.35), (2.55, 0.2))])
        t_en = self.clk.get_value()

        def ondas():
            t = self.clk.get_value() - t_en
            g = VGroup()
            for k in range(3):
                ph = (t / 2.4 + k / 3) % 1.0
                g.add(Circle(radius=2.2 + 0.6 * ph).move_to(P3(0, 1.0)).set_stroke(VEL, 3.2, opacity=0.5 * math.sin(math.pi * ph)))
            return g
        ov = vivo(ondas)
        ins = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 32, bold=True).move_to(P3(0, -2.6))
        self.play(FadeIn(logo, scale=0.95), FadeIn(aneis), FadeIn(ov), run_time=0.7)
        self.gat("se inscreve no canal")
        self.play(FadeIn(ins, shift=0.1 * UP), run_time=0.7)
        self.foco = ins
        self.ate(0.99)
        # ── EN2: o desafio na rampa ──
        self.an("EN2")
        self.secao("DESAFIO")
        ov.clear_updaters()
        A0, A1 = P3(-6.4, 1.2), P3(-0.6, -2.6)
        ramp = Polygon(A0, A1, P3(A0[0], A1[1])).set_z_index(3)
        aco(ramp, 1.8)
        u = (A1 - A0) / np.linalg.norm(A1 - A0)
        nrm = np.array([-u[1], u[0], 0])
        rc = 0.62
        c_m = A0 + 1.3 * u + nrm * rc
        c_o = A0 + 2.9 * u + nrm * rc
        mac = VGroup(disco_aco(c_m, rc), Circle(radius=rc).move_to(c_m).set_stroke(width=0).set_fill(MAS, 0.4).set_z_index(6), Dot(c_m, radius=0.05, color=WHITE_).set_z_index(7))
        oco = VGroup(aro2d(c_o, rc - 0.05, 0.1), Dot(c_o, radius=0.05, color=WHITE_).set_z_index(7))
        lmac = txt("MACIÇO", 24).move_to(c_m + P3(-0.1, 1.15))
        loco = txt("OCO", 24).move_to(c_o + P3(0.55, 1.15))
        d1_ = txt("DESAFIO:", 34, bold=True, color=CYAN).move_to(P3(3.4, 1.9))
        d2_ = VGroup(txt("QUEM CHEGA PRIMEIRO,", 34, bold=True), txt("ROLANDO SEM ESCORREGAR?", 34, bold=True)).arrange(DOWN, buff=0.18).next_to(d1_, DOWN, buff=0.35)
        d3_ = VGroup(txt("MESMA MASSA, MESMO RAIO", 26), VGroup(txt("USE O FATOR", 26), MathTex("c", font_size=46, color=MAS), txt("DA TABELA", 26)).arrange(RIGHT, buff=0.14)) \
            .arrange(DOWN, buff=0.16).next_to(d2_, DOWN, buff=0.4)
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(ov), FadeOut(ins), run_time=0.4)
        self.play(FadeIn(ramp), FadeIn(mac), FadeIn(oco), FadeIn(d2_, shift=0.1 * UP), run_time=0.7)      # v5: sem o "DESAFIO:" repetido (o canto já diz)
        self.gat("um cilindro maciço")
        self.play(FadeIn(lmac), self.ind_copia(mac, WHITE_, 1.1, 0.7), run_time=0.7)
        self.gat("e um cilindro oco de parede fina")
        self.play(FadeIn(loco), self.ind_copia(oco, WHITE_, 1.1, 0.7), run_time=0.7)
        self.gat("quem chega primeiro")
        self.play(Indicate(d2_, scale_factor=1.04, color=WHITE_), run_time=0.7)
        self.gat("usa o fator da tabela")
        self.play(FadeIn(d3_, shift=0.1 * UP), run_time=0.7)
        self.foco = d2_
        self.vivos = [ramp]
        dd_ = 2.0                                                          # v6 §5: largada — as duas rolam um pouco e a imagem congela (sem mostrar o resultado)
        mac0, oco0 = mac.copy(), oco.copy()

        def rola(m_, m0_):
            def f(mm, a):
                mm.become(m0_)
                mm.shift(u * dd_ * a)
                mm.rotate(-dd_ * a / rc)
            return UpdateFromAlphaFunc(m_, f)
        self.play(rola(mac, mac0), rola(oco, oco0), Succession(ApplyWave(d2_, amplitude=0.12, run_time=1.6), ApplyWave(d3_, amplitude=0.12, run_time=1.6), ApplyWave(d2_, amplitude=0.12, run_time=1.6)), run_time=max(1.2, self.resta() - 0.5), rate_func=rate_functions.linear)
        self.ate(0.99)
