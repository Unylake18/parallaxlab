"""Lote PS (v2): S1 (cinco cartões grandes, um por vez, com o disco girando atrás), S2 (a régua 3D do hook volta com o mesmo dolly-in e em câmera lenta,
com a reta a(r), a marca 2L/3 ≈ 67 cm e a força M g / 4 na dobradiça), EN1 (encerramento: logo, três ícones giratórios do módulo de exercícios de rotação,
INSCREVA-SE) e EN2 (desafio: régua 3D com massa extra rosa e moeda; solta nos últimos 3 s e congela antes de revelar). A solução (9g/8) não aparece."""
from pecas22 import *  # noqa: F401,F403


def cartao_(conteudo, cor, w=6.8):
    bx = RoundedRectangle(corner_radius=0.12, width=max(w, conteudo.width + 0.6), height=conteudo.height + 0.46).move_to(conteudo).set_fill(PANEL, 0.88).set_stroke(cor, 2.6)
    bx._fundo = bx._caixa = True
    return VGroup(bx, conteudo).set_z_index(20)


def icone_polia(c, t_in, clk):
    """Polia com massa: roda de 6 raios girando, corda e bloco rosa pendurado."""
    def f():
        a = 0.62 * (clk.get_value() - t_in)
        roda_ = Circle(radius=0.62).set_stroke(GEO, 4).set_fill(PANEL, 0.9)
        raios = VGroup(*[Line(ORIGIN, 0.58 * np.array([math.cos(a + k * PI / 3), math.sin(a + k * PI / 3), 0])).set_stroke(GEO, 3) for k in range(6)])
        g = VGroup(roda_, raios).move_to(c + 0.55 * UP)
        corda = Line(c + P3(-0.62, 0.55), c + P3(-0.62, -0.55)).set_stroke(GEO, 3)
        corda2 = Line(c + P3(0.62, 0.55), c + P3(0.62, -0.10)).set_stroke(GEO, 3)
        bloco = Square(0.5).set_fill(MAS, 0.9).set_stroke(MAS, 2).move_to(c + P3(-0.62, -0.80))
        bloco2 = Square(0.3).set_fill(MAS, 0.9).set_stroke(MAS, 2).move_to(c + P3(0.62, -0.25))
        return VGroup(g, corda, corda2, bloco, bloco2).scale(1.25, about_point=c)
    return vivo(f)


def icone_pino(c, t_in, clk):
    """Pino/dobradiça com seta de força que pulsa."""
    def f():
        a = clk.get_value() - t_in
        pulso = 1.0 + 0.12 * math.sin(2 * PI * 0.6 * a)
        base = Rectangle(width=1.6, height=0.22).set_fill(PANEL, 0.95).set_stroke(GEO, 3).move_to(c + P3(0, -0.55))
        pino = Circle(radius=0.28).set_stroke(GEO, 4).set_fill("#8E9BAE", 0.9).move_to(c + P3(0, -0.20))
        sh = a * 0.62
        cruz = VGroup(Line(P3(-0.2, 0), P3(0.2, 0)), Line(P3(0, -0.2), P3(0, 0.2))).set_stroke(PANEL, 3).rotate(sh).move_to(pino)
        s_ = Arrow(c + P3(0, -0.20), c + P3(0, -0.20 + 1.15 * pulso), buff=0, color=FC, stroke_width=7, max_tip_length_to_length_ratio=0.35)
        return VGroup(base, pino, cruz, s_).scale(1.25, about_point=c)
    return vivo(f)


def icone_disco(c, t_in, clk):
    """Disco freando por atrito: gira, pastilha e faíscas piscando."""
    def f():
        a = 0.62 * (clk.get_value() - t_in)
        cd = c + P3(0, 0.15)
        d = VGroup(Circle(radius=0.72).set_stroke(GEO, 4).set_fill(PANEL, 0.9).move_to(cd),
                   *[Sector(radius=0.68, angle=PI / 4, start_angle=a + k * PI, arc_center=cd).set_fill(MAS, 0.55).set_stroke(width=0) for k in range(2)])
        pad = Rectangle(width=0.5, height=0.22).set_fill("#8E9BAE", 0.95).set_stroke(GEO, 2).move_to(cd + P3(0.72 + 0.22, 0))
        fa = VGroup()
        tt = clk.get_value() - t_in
        for k in range(5):
            ph = (tt * 2.2 + k * 0.2) % 1.0
            ang = -0.5 + 0.25 * k
            p0 = cd + P3(0.72, 0) * 1.0 + 0.0
            fa.add(Line(p0 + 0.05 * RIGHT, p0 + (0.15 + 0.5 * ph) * np.array([math.cos(ang), math.sin(ang), 0])).set_stroke(ACC, 3, opacity=1 - ph))
        return VGroup(d, pad, fa).scale(1.25, about_point=c)
    return vivo(f)


class LoteFim(Lote22):
    def corpo(self):
        # ── S1: cinco cartões grandes, um por vez, com o disco girando atrás ──
        self.an("S1")
        self.secao("SÍNTESE")

        def formula(s, fs=56):
            m = MathTex(s, font_size=fs)
            tinge(m)
            return m

        c1 = cartao_(VGroup(txt("BRAÇO DE ALAVANCA", 36, bold=True, color=TQ), formula(r"\tau = r_\perp F = r F_\perp")).arrange(DOWN, buff=0.25), TQ, w=8.2)
        c2 = cartao_(VGroup(txt("DEPENDE DO PONTO ESCOLHIDO", 36, bold=True, color=TQ), formula(r"\vec\tau = \vec r \times \vec F")).arrange(DOWN, buff=0.25), TQ, w=8.2)
        c3 = cartao_(VGroup(txt("EIXO FIXO OU PELO CM, NO PLANO", 36, bold=True, color=MAS), formula(r"\sum\tau_{\mathrm{ext},z} = I_z\alpha")).arrange(DOWN, buff=0.25), MAS, w=8.2)
        c4 = cartao_(VGroup(txt("TRABALHO E POTÊNCIA", 36, bold=True, color=KC), formula(r"W = \int\tau\,d\theta"), formula(r"P = \tau\omega")).arrange(DOWN, buff=0.22), KC, w=8.2)
        c5 = cartao_(VGroup(txt("EQUILÍBRIO ESTÁTICO", 36, bold=True, color=GEO), formula(r"\sum\vec F = \vec 0"), formula(r"\sum\vec\tau = \vec 0")).arrange(DOWN, buff=0.22), GEO, w=8.2)
        cs = [c1, c2, c3, c4, c5]
        for c_ in cs:
            c_.move_to(P3(2.95, -0.35))

        t0 = self.clk.get_value()
        CD = P3(-5.15, -0.35)
        dv = vivo(lambda: VGroup(
            DiscoPedacos(CD, 1.8, 4, 10).rotate(0.35 * (self.clk.get_value() - t0), about_point=CD),
            eixo_cruz(CD, 0.15),
            arco_torque(CD, 2.12, 1, 0.3, 1.4, TQ, w=5),
        ))
        self.play(FadeIn(dv), run_time=0.6)

        frases_s1 = (
            "um torque é força vezes braço",
            "dois ele é um vetor",
            "três a segunda lei da rotação",
            "quatro o trabalho é a integral",
            "cinco equilíbrio estático",
        )
        atual = None
        for c_, fr in zip(cs, frases_s1):
            self.gat(fr)
            if atual is None:
                self.play(FadeIn(c_, shift=0.10 * UP), run_time=0.7)
            else:
                self.play(FadeOut(atual), run_time=0.3)
                self.play(FadeIn(c_, shift=0.10 * UP), run_time=0.5)
            atual = c_
            self.foco = c_
        self.ate(0.99)

        # ── S2: a régua 3D do hook volta com o mesmo dolly-in, em câmera lenta ──
        self.an("S2")
        self.secao("A RESPOSTA DA RÉGUA")
        u_s2 = ValueTracker(0.0)
        t_s2 = ValueTracker(0.0)
        massa_p = ValueTracker(0.0)
        self.add(u_s2, t_s2, massa_p)

        def est_s2(t):
            tf = float(min(0.15, max(0.0, t_s2.get_value())))
            mp_flag = bool(massa_p.get_value() > 0.5)
            cam = cam_hook(u_s2.get_value())
            e = estado_regua(tf, massa_ponta=mp_flag, moedas=True)
            e["cam"] = cam
            if not PEDIDOS3D:
                idx = min(1500, max(0, int(round(tf / 1e-4))))
                th = float(TAB_REGUA["th_en2"][idx] if mp_flag else TAB_REGUA["th"][idx])
                self.reg(
                    "s2_regua",
                    t_fis=tf,
                    massa_ponta=mp_flag,
                    dobradica=tela_regua(cam, 0.0, th),
                    cm=tela_regua(cam, 0.50, th),
                    dois_tercos=tela_regua(cam, 2.0 / 3.0, th),
                    ponta=tela_regua(cam, 1.00, th),
                )
            return r4(e)

        f3 = Fundo3D(self, "regua", est_s2, op=0.0)
        self.add(f3)
        dv.clear_updaters()
        self.troca([dv, atual], f3.op.animate.set_value(1.0), seq=True)

        # dolly-in (3/4 → frontal) e depois a queda lenta até 0,15 s, com o rastro estroboscópico
        self.play(u_s2.animate.set_value(1.0), run_time=6.0, rate_func=smooth)
        cam_s2 = cam_hook(1.0)
        th_15 = float(TAB_REGUA["th"][1500])
        idxs = [int(round(0.025 * k / 1e-4)) for k in range(1, 7)]
        fant = VGroup(*[
            Line(P3(*tela_regua(cam_s2, 0.0, float(TAB_REGUA["th"][i])), 0.0), P3(*tela_regua(cam_s2, 1.0, float(TAB_REGUA["th"][i])), 0.0)).set_stroke(TQ, 2.2, opacity=0.2 + 0.05 * k).set_z_index(5)
            for k, i in enumerate(idxs, 1)])
        self.play(t_s2.animate.set_value(0.15), LaggedStart(*[FadeIn(f_) for f_ in fant], lag_ratio=0.8), run_time=3.6, rate_func=linear)

        p_dob = P3(*tela_regua(cam_s2, 0.0, th_15), 0.0)
        p_meio = P3(*tela_regua(cam_s2, 0.50, th_15), 0.0)
        p_23 = P3(*tela_regua(cam_s2, 2.0 / 3.0, th_15), 0.0)
        p_ponta = P3(*tela_regua(cam_s2, 1.00, th_15), 0.0)
        p_m2 = P3(*projeta3d(cam_s2, (float(TAB_REGUA["m2x"][1500]), 0.0, float(TAB_REGUA["m2z"][1500]))), 0.0)

        # reta a(r) verde, marca de 2L/3 (laser vertical sobre o g), setas e reação M g / 4 na dobradiça
        s_dob_s2 = seta(p_dob + UP * 0.30, p_dob + UP * 1.55, FC, 6, tip=0.22)
        l_dob_s2 = T(r"\tfrac{1}{4}Mg", 46, FC).next_to(s_dob_s2, RIGHT, buff=0.16)
        s_m_s2 = seta(p_meio + DOWN * 0.22, p_meio + DOWN * 0.95, ACC, 5.5, tip=0.18)
        s_23_s2 = seta(p_23 + DOWN * 0.22, p_23 + DOWN * 1.25, ACC, 5.5, tip=0.18)
        s_pt_s2 = seta(p_ponta + DOWN * 0.22, p_ponta + DOWN * 1.85, ACC, 6, tip=0.20)
        reta_s2 = DashedLine(p_dob, p_ponta + DOWN * 1.85, dash_length=0.09).set_stroke(ACC, 2.8)
        laser = DashedLine(p_23 + 1.1 * UP, p_23 + DOWN * 1.8, dash_length=0.12).set_stroke(GEO, 2.4)
        lbl_23_s2 = VGroup(T(r"\tfrac{2}{3}L", 40, GEO), T("a_t = g", 40, ACC)).arrange(RIGHT, buff=0.25).next_to(laser, UP, buff=0.35)
        lbl_pt_s2 = T(r"\tfrac{3}{2}g", 46, ACC).next_to(s_pt_s2, RIGHT, buff=0.16)

        card_s2 = cartao_(
            VGroup(
                MathTex(r"|\alpha| = \frac{3g}{2L},\quad a_t(r) = \frac{3g}{2L}r", font_size=46),
                MathTex(r"r = \frac{2}{3}L \Rightarrow a_t = g", font_size=46),
            ).arrange(DOWN, buff=0.2),
            ACC,
            w=6.0,
        ).move_to(P3(-3.8, -2.68))
        tinge(card_s2[1][0])
        tinge(card_s2[1][1])

        self.gat("proporção da distância ao eixo")
        self.play(FadeIn(card_s2, shift=0.1 * DOWN), Create(reta_s2), FadeIn(s_m_s2), FadeIn(s_23_s2), run_time=0.9)

        self.gat("dois terços do comprimento")
        self.play(Create(laser), FadeIn(lbl_23_s2), run_time=0.8)

        self.gat("os vizinhos puxam a ponta")
        self.play(FadeIn(s_dob_s2), FadeIn(l_dob_s2), run_time=0.7)
        self.gat("na ponta três meios de g")
        self.play(FadeIn(s_pt_s2), FadeIn(lbl_pt_s2), run_time=0.6)
        self.foco = card_s2
        self.ate(0.99)

        # ── EN1: encerramento (logo + três ícones do módulo de exercícios de rotação + INSCREVA-SE) ──
        self.an("EN1")
        velhos = self.snap()
        self.play(
            *[m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in velhos if not isinstance(m, ValueTracker)],
            run_time=0.5,
        )
        self.secao(None)
        CL = P3(0, 3.0)
        logo = self.logo(3.8).move_to(CL)
        t_en = self.clk.get_value()

        def ondas():
            t = self.clk.get_value() - t_en
            g = VGroup()
            for k in range(3):
                ph = (t / 2.4 + k / 3) % 1.0
                g.add(Circle(radius=0.75 + 0.30 * ph).move_to(CL).set_stroke(VEL, 3.0, opacity=0.5 * math.sin(math.pi * ph)))
            return g

        ov = vivo(ondas)
        ins = VGroup(txt("INSCREVA-SE PARA ACOMPANHAR", 46, bold=True), txt("OS PRÓXIMOS VÍDEOS", 46, bold=True)).arrange(DOWN, buff=0.12).move_to(P3(0, -3.28))
        self.play(FadeIn(logo, scale=0.95), FadeIn(ov), run_time=0.7)
        self.gat("se inscreve no canal")
        self.play(FadeIn(ins, shift=0.1 * UP), run_time=0.7)

        legenda = txt("AGORA COLOCA O TORQUE PARA TRABALHAR", 38, bold=True, color=TQ).move_to(P3(0, -2.1))
        xs = (-4.6, 0.0, 4.6)
        yi = 0.40
        icones = [icone_polia(P3(xs[0], yi), self.clk.get_value(), self.clk),
                  icone_pino(P3(xs[1], yi), self.clk.get_value(), self.clk),
                  icone_disco(P3(xs[2], yi), self.clk.get_value(), self.clk)]
        rots = [txt("POLIA COM MASSA", 36, bold=True, color=MAS).move_to(P3(xs[0], -1.3)),
                txt("FORÇA NO PINO", 36, bold=True, color=FC).move_to(P3(xs[1], -1.3)),
                txt("DISCO FREADO", 36, bold=True, color=ACC).move_to(P3(xs[2], -1.3))]
        self.gat("a gente coloca tudo isso")
        self.play(FadeIn(legenda, shift=0.1 * UP), run_time=0.6)
        for ic, rt_, fr in zip(icones, rots, ("polia que tem massa", "a força que o pino faz", "um disco sendo freado")):
            self.gat(fr)
            self.play(FadeIn(ic, scale=0.9), FadeIn(rt_, shift=0.08 * UP), run_time=0.7)
        self.gat("um desafio pra você")
        self.play(Indicate(ins, color=ACC, scale_factor=1.04), run_time=0.9)
        self.foco = ins
        self.ate(0.99)

        # ── EN2: desafio — régua 3D com massa extra rosa e moeda; solta nos últimos 3 s e congela ──
        self.an("EN2")
        self.poeira_extra(n=150, seed=7, vmul=2.6, opm=1.6)     # desafio: cena parada por ~18 s; poeira mais viva mantém a tela em movimento (PARADO)
        self.secao("DESAFIO")
        ov.clear_updaters()
        t_s2.set_value(0.0)
        massa_p.set_value(1.0)

        p_bloco = P3(*tela_regua(cam_s2, 0.96, 0.0, dz=0.03), 0.0)
        lbl_bloco = VGroup(txt("MASSA EXTRA:", 32, bold=True, color=MAS), T("M", 48, MAS)).arrange(RIGHT, buff=0.14).move_to(P3(4.6, -1.45))
        ch_bloco = Line(lbl_bloco.get_top() + 0.22 * UP + 0.5 * LEFT, p_bloco + P3(0.0, -0.32)).set_stroke(MAS, 2.4)
        d_card = cartao_(
            VGroup(
                txt("DESAFIO", 36, bold=True, color=MAS),
                linha_base([txt("A PONTA AINDA ACELERA MAIS QUE", 36, bold=True, color=ACC), T("g", 46, ACC), txt("?", 36, bold=True, color=ACC)], 0.24),
            ).arrange(DOWN, buff=0.18),
            MAS,
            w=7.4,
        ).move_to(P3(-1.8, 2.2))

        self.play(FadeOut(logo), FadeOut(ov), FadeOut(ins), FadeOut(legenda), *[FadeOut(x) for x in (*icones, *rots)], f3.op.animate.set_value(1.0), run_time=0.7)
        self.gat("prende na ponta da régua")
        self.play(FadeIn(lbl_bloco, shift=0.1 * DOWN), Create(ch_bloco), run_time=0.8)

        self.gat("ainda acelera mais que a gravidade")
        self.play(FadeIn(d_card, shift=0.1 * UP), run_time=0.8)

        # Nos últimos ~3 s solta a régua por um curtíssimo instante (t = 0 → 0,035 s) e congela com "?" antes de revelar
        self.gat("resposta nos comentários")
        interrog = T("?", 72, ACC).move_to(p_bloco + P3(0.9, -0.9))
        self.play(t_s2.animate.set_value(0.035), FadeIn(interrog, scale=1.2), run_time=1.2, rate_func=linear)
        self.foco = d_card
        self.ate(0.99)
