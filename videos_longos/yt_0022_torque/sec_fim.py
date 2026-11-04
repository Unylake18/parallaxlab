"""Lote PS: S1 (cinco cartões PANEL de resumo na direita + palco 2,5D vivo na esquerda), S2 (Three.js 'regua' em câmera lenta até t = 0,15 s,
sobreposta à reta de aceleração a(r), à marca 2L/3 ≈ 67 cm e à força M g / 4 na dobradiça), EN1 (encerramento padrão: logo com anéis violeta e
INSCREVA-SE), EN2 (desafio com bloco extra de massa M preso na ponta da régua e moeda em cima; solta nos últimos 3 s e congela antes de revelar)."""
from pecas22 import *  # noqa: F401,F403


def cartao_(conteudo, cor, w=6.8):
    bx = RoundedRectangle(corner_radius=0.12, width=max(w, conteudo.width + 0.5), height=conteudo.height + 0.34).move_to(conteudo).set_fill(PANEL, 0.86).set_stroke(cor, 2.4)
    bx._fundo = bx._caixa = True
    return VGroup(bx, conteudo).set_z_index(20)


class LoteFim(Lote22):
    def corpo(self):
        # ── S1: cinco cartões de síntese + palco 2,5D vivo ──
        self.an("S1")
        self.secao("SÍNTESE")

        c1 = cartao_(MathTex(r"\tau = r F\sin\varphi = r_\perp F = r F_\perp", font_size=36), TQ)
        tinge(c1[1])
        c2 = cartao_(MathTex(r"\vec\tau = \vec r \times \vec F", font_size=38), TQ)
        tinge(c2[1])
        c3 = cartao_(MathTex(r"\sum\tau_{\mathrm{ext},z} = I_z\alpha", font_size=38), TQ)
        tinge(c3[1])
        c4 = cartao_(MathTex(r"W = \int\tau\,d\theta = \Delta K_{\mathrm{rot}},\quad P = \tau\omega", font_size=34), KC)
        tinge(c4[1])
        c5 = cartao_(MathTex(r"\text{EQUILÍBRIO: }\sum\vec F = \vec 0\ \text{ E }\ \sum\vec\tau = \vec 0", font_size=34), GEO)
        tinge(c5[1])

        cs = VGroup(c1, c2, c3, c4, c5).arrange(DOWN, buff=0.18).move_to(P3(2.4, -0.45))

        t0 = self.clk.get_value()
        CD = P3(-4.4, -0.45)
        dv = vivo(lambda: VGroup(
            DiscoPedacos(CD, 1.75, 4, 10).rotate(0.35 * (self.clk.get_value() - t0), about_point=CD),
            eixo_cruz(CD, 0.15),
            arco_torque(CD, 2.05, 1, 0.3, 1.4, TQ, w=5),
        ))
        self.play(FadeIn(dv), run_time=0.6)

        frases_s1 = (
            "um torque é força vezes braço",
            "dois ele é um vetor",
            "três a segunda lei da rotação",
            "quatro o trabalho é a integral",
            "cinco equilíbrio estático",
        )
        for c_, fr in zip(cs, frases_s1):
            self.gat(fr)
            self.play(FadeIn(c_, shift=0.10 * UP), run_time=0.65)
            self.foco = c_
        self.ate(0.99)

        # ── S2: a resposta da régua (Three.js 'regua' + reta a(r), marca 2L/3 e força M g / 4 na dobradiça) ──
        self.an("S2")
        self.secao("A RESPOSTA DA RÉGUA")
        cam_s2 = cam_regua_frente()
        t_s2 = ValueTracker(0.0)
        massa_p = ValueTracker(0.0)
        self.add(t_s2, massa_p)

        def est_s2(t):
            tf = float(min(0.15, max(0.0, t_s2.get_value())))
            mp_flag = bool(massa_p.get_value() > 0.5)
            e = estado_regua(tf, massa_ponta=mp_flag, moedas=True)
            e["cam"] = cam_s2
            if not PEDIDOS3D:
                idx = min(1500, max(0, int(round(tf / 1e-4))))
                th = float(TAB_REGUA["th_en2"][idx] if mp_flag else TAB_REGUA["th"][idx])
                self.reg(
                    "s2_regua",
                    t_fis=tf,
                    massa_ponta=mp_flag,
                    dobradica=tela_regua(cam_s2, 0.0, th),
                    cm=tela_regua(cam_s2, 0.50, th),
                    dois_tercos=tela_regua(cam_s2, 2.0 / 3.0, th),
                    ponta=tela_regua(cam_s2, 1.00, th),
                )
            return r4(e)

        f3 = Fundo3D(self, "regua", est_s2, op=0.0)
        self.add(f3)
        dv.clear_updaters()
        self.troca([dv, *cs], f3.op.animate.set_value(1.0), seq=True)

        # Queda lenta até 0,15 s
        self.play(t_s2.animate.set_value(0.15), run_time=2.2, rate_func=linear)

        th_15 = float(TAB_REGUA["th"][1500])
        p_dob = P3(*tela_regua(cam_s2, 0.0, th_15), 0.0)
        p_meio = P3(*tela_regua(cam_s2, 0.50, th_15), 0.0)
        p_23 = P3(*tela_regua(cam_s2, 2.0 / 3.0, th_15), 0.0)
        p_ponta = P3(*tela_regua(cam_s2, 1.00, th_15), 0.0)

        # Marca de 2L/3 ≈ 67 cm, setas de aceleração (0,75g, g, 3g/2) e reação M g / 4 na dobradiça
        s_dob_s2 = seta(p_dob + UP * 0.15, p_dob + UP * 1.15, FC, 6, tip=0.20)
        l_dob_s2 = T(r"\tfrac{1}{4}Mg", 36, FC).next_to(s_dob_s2, UP, buff=0.14)
        s_m_s2 = seta(p_meio + DOWN * 0.08, p_meio + DOWN * 0.85, ACC, 5.5, tip=0.18)
        s_23_s2 = seta(p_23 + DOWN * 0.08, p_23 + DOWN * 1.10, ACC, 5.5, tip=0.18)
        s_pt_s2 = seta(p_ponta + DOWN * 0.08, p_ponta + DOWN * 1.65, ACC, 6, tip=0.20)
        reta_s2 = DashedLine(p_dob, p_ponta + DOWN * 1.65, dash_length=0.09).set_stroke(ACC, 2.8)
        lbl_23_s2 = VGroup(T(r"\tfrac{2}{3}L", 36, GEO), T("a_t = g", 36, ACC)).arrange(DOWN, buff=0.06).move_to(p_23 + P3(-0.35, 0.55))
        lbl_pt_s2 = T(r"\tfrac{3}{2}g", 38, ACC).next_to(s_pt_s2, RIGHT, buff=0.16)

        card_s2 = cartao_(
            VGroup(
                MathTex(r"|\alpha| = \frac{3g}{2L},\quad a_t(r) = \frac{3g}{2L}r", font_size=38),
                MathTex(r"r = \frac{2}{3}L \Rightarrow a_t = g,\quad a_{\mathrm{ponta}} = \frac{3}{2}g", font_size=36),
            ).arrange(DOWN, buff=0.16),
            ACC,
            w=5.0,
        ).move_to(P3(4.15, 1.85))
        tinge(card_s2[1][0])
        tinge(card_s2[1][1])

        self.gat("proporção da distância ao eixo")
        self.play(FadeIn(card_s2, shift=0.1 * DOWN), Create(reta_s2), FadeIn(s_m_s2), FadeIn(s_23_s2), FadeIn(s_pt_s2), FadeIn(lbl_pt_s2), run_time=0.9)

        self.gat("dois terços do comprimento")
        self.play(FadeIn(lbl_23_s2), run_time=0.7)

        self.gat("os vizinhos puxam a ponta")
        self.play(FadeIn(s_dob_s2), FadeIn(l_dob_s2), run_time=0.7)
        self.foco = card_s2
        self.ate(0.99)

        # ── EN1: encerramento padrão (logo + ondas + INSCREVA-SE) ──
        self.an("EN1")
        velhos = self.snap()
        self.play(
            *[m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in velhos if not isinstance(m, ValueTracker)],
            run_time=0.5,
        )
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

        # ── EN2: desafio — bloco extra de massa M preso na ponta da régua + moeda sobre ele ──
        self.an("EN2")
        self.secao("DESAFIO")
        ov.clear_updaters()
        t_s2.set_value(0.0)
        massa_p.set_value(1.0)

        p_bloco = P3(*tela_regua(cam_s2, 0.96, 0.0, dz=0.025), 0.0)
        lbl_bloco = VGroup(txt("MASSA EXTRA:", 24, bold=True, color=MAS), T("M", 40, MAS)).arrange(RIGHT, buff=0.12).move_to(p_bloco + P3(-1.35, 0.72))
        d_card = cartao_(
            VGroup(
                txt("BLOCO DE MASSA M NA PONTA + MOEDA", 22, bold=True, color=MAS),
                txt("A PONTA AINDA ACELERA MAIS QUE g ?", 26, bold=True, color=ACC),
                txt("QUAL É A NOVA ACELERAÇÃO DA PONTA?", 22, color=GEO),
            ).arrange(DOWN, buff=0.16),
            MAS,
            w=5.4,
        ).move_to(P3(3.95, 1.55))

        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(ov), FadeOut(ins), f3.op.animate.set_value(1.0), run_time=0.6)
        self.gat("prende na ponta da régua")
        self.play(FadeIn(lbl_bloco, shift=0.1 * DOWN), run_time=0.7)

        self.gat("ainda acelera mais que a gravidade")
        self.play(FadeIn(d_card, shift=0.1 * UP), run_time=0.8)

        # Nos últimos ~3 s solta a régua por um curtíssimo instante (t = 0 → 0,035 s) e congela com "?" antes de revelar
        self.gat("resposta nos comentários")
        interrog = T("?", 68, ACC).move_to(p_bloco + P3(0.55, -0.55))
        self.play(t_s2.animate.set_value(0.035), FadeIn(interrog, scale=1.2), run_time=1.2, rate_func=linear)
        self.foco = d_card
        self.ate(0.99)
