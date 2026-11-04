"""Lote PH: hook H1–H3 (Three.js 'regua'). Régua metálica de 1,0 m presa numa dobradiça horizontal na beira da bancada, com duas moedas
sobre ela (meio a 50 cm e ponta a 100 cm). A câmera começa a 3/4, desce até a vista frontal pura e PARA antes de qualquer seta ou cota.
Em H2, queda em câmera lenta ×10 de t = 0 até t = 0,15 s (θ = 9,5°, folga de 5,4 cm na ponta em lupa ×3; moeda do meio segue colada,
iniciando escorregamento em ~2,9° com N > 0). Setas verdes de aceleração comparam g, 3g/2 e 0,75g. Em H3, a pergunta central apresenta o TORQUE (τ)."""
from pecas22 import *  # noqa: F401,F403


class LoteHook(Lote22):
    def corpo(self):
        t_fis = ValueTracker(0.0)
        u_cam = ValueTracker(0.0)
        self.add(t_fis, u_cam)

        def est(t):
            tf = min(0.15, max(0.0, t_fis.get_value()))
            cam = cam_regua_obl(u_cam.get_value())
            e = estado_regua(tf)
            e["cam"] = cam
            if not PEDIDOS3D:
                idx = min(1500, max(0, int(round(tf / 1e-4))))
                th = float(TAB_REGUA["th"][idx])
                self.reg(
                    "hook_regua",
                    t_fis=tf,
                    th_deg=math.degrees(th),
                    folga_cm=float(TAB_REGUA["folga2"][idx]) * 100.0,
                    nm1=float(TAB_REGUA["nm1"][idx]),
                    r1=float(TAB_REGUA["r1"][idx]),
                    dobradica=tela_regua(cam, 0.0, th),
                    cm=tela_regua(cam, 0.50, th),
                    dois_tercos=tela_regua(cam, 2.0 / 3.0, th),
                    ponta=tela_regua(cam, 1.00, th),
                    moeda_meio=projeta3d(cam, (float(TAB_REGUA["m1x"][idx]), 0.0, float(TAB_REGUA["m1z"][idx]))),
                    moeda_ponta=projeta3d(cam, (float(TAB_REGUA["m2x"][idx]), 0.0, float(TAB_REGUA["m2z"][idx]))),
                )
            return r4(e)

        f3 = Fundo3D(self, "regua", est)
        self.add(f3)
        self.f3 = f3
        self.secao("A RÉGUA E AS DUAS MOEDAS")
        for a_ in list(self._pend):
            if getattr(a_, "mobject", None) is self.h2:
                self._pend.remove(a_)
                self.add(self.h2)

        # ── H1: apresentação do experimento; câmera 3/4 desce até frontal pura e PARA ──
        self.an("H1")
        self.play(u_cam.animate.set_value(1.0), run_time=3.6, rate_func=smooth)
        cam_f = cam_regua_frente()
        p_dob = P3(*tela_regua(cam_f, 0.0, 0.0), 0.0)
        p_meio = P3(*tela_regua(cam_f, 0.50, 0.0), 0.0)
        p_ponta = P3(*tela_regua(cam_f, 1.00, 0.0), 0.0)

        # Cota L = 1,0 m abaixo da régua + destaque colorido na dobradiça e cartão de apresentação à direita
        cota_L = VGroup(
            Line(p_dob + 0.52 * DOWN, p_ponta + 0.52 * DOWN).set_stroke(TQ, 3.2),
            Line(p_dob + 0.40 * DOWN, p_dob + 0.64 * DOWN).set_stroke(TQ, 3.2),
            Line(p_ponta + 0.40 * DOWN, p_ponta + 0.64 * DOWN).set_stroke(TQ, 3.2),
            VGroup(MathTex("L=", font_size=40, color=GEO), nm(r"1{,}0\ \mathrm{m}", GEO, 40)).arrange(RIGHT, buff=0.1).move_to((p_dob + p_ponta) / 2 + 0.92 * DOWN),
        ).set_z_index(12)
        anel_dob = Circle(radius=0.22).move_to(p_dob).set_stroke(TQ, 3.4)
        lbl_dob = txt("DOBRADIÇA", 24, bold=True, color=TQ).move_to(p_dob + P3(-0.35, 0.62))
        dedo = dedo_silhueta(p_ponta + 0.08 * DOWN, dir_dedo=UP, comp=0.92)
        dedo.set_stroke(FC, 3.0)
        self.play(FadeIn(cota_L), FadeIn(anel_dob), FadeIn(lbl_dob), FadeIn(dedo), run_time=0.8)

        self.gat("duas moedas")
        lbl_m2 = txt("PONTA (100 cm)", 24, bold=True, color=ACC).move_to(p_ponta + P3(0.0, 0.68))
        lbl_m1 = txt("MEIO (50 cm)", 24, bold=True, color=ACC).move_to(p_meio + P3(0.0, 0.68))
        self.play(FadeIn(lbl_m2, shift=0.1 * DOWN), FadeIn(lbl_m1, shift=0.1 * DOWN), run_time=0.7)

        self.gat("tirar o dedo")
        self.play(FadeOut(dedo, shift=0.35 * DOWN), FadeOut(cota_L), run_time=0.6)

        self.gat("as moedas vão junto")
        self.selo("PERGUNTA", "AS MOEDAS DESCEM JUNTO COM A RÉGUA?")
        anel1 = Circle(radius=0.24).move_to(p_meio + 0.05 * UP).set_stroke(ACC, 3.2)
        anel2 = Circle(radius=0.24).move_to(p_ponta + 0.05 * UP).set_stroke(ACC, 3.2)
        self.play(FadeIn(anel1), FadeIn(anel2), run_time=0.4)
        self.play(anel1.animate.scale(1.18), anel2.animate.scale(1.18), rate_func=there_and_back, run_time=0.9)
        self.play(FadeOut(anel1), FadeOut(anel2), FadeOut(anel_dob), FadeOut(lbl_dob), FadeOut(lbl_m1), FadeOut(lbl_m2), run_time=0.4)
        self.foco = f3
        self.ate(0.99)

        # ── H2: largada em câmera lenta ×10 (0 → 0,15 s), lupa ×3 na ponta (5,4 cm) e setas verdes de aceleração ──
        self.an("H2")
        self.selo("CÂMERA LENTA ×10", "QUEDA DE 0 A 0,15 s")
        # Queda física de 0 a 0,15 s em câmera lenta
        self.play(t_fis.animate.set_value(0.15), run_time=3.2, rate_func=linear)

        th_15 = float(TAB_REGUA["th"][1500])
        p_m1_15 = P3(*projeta3d(cam_f, (float(TAB_REGUA["m1x"][1500]), 0.0, float(TAB_REGUA["m1z"][1500]))), 0.0)
        p_m2_15 = P3(*projeta3d(cam_f, (float(TAB_REGUA["m2x"][1500]), 0.0, float(TAB_REGUA["m2z"][1500]))), 0.0)
        p_pt_15 = P3(*tela_regua(cam_f, 1.0, th_15), 0.0)

        tag_meio = txt("SEGUE ENCOSTADA", 24, bold=True, color=ACC).move_to(p_m1_15 + P3(-0.2, 0.65))
        self.play(FadeIn(tag_meio, shift=0.08 * DOWN), run_time=0.6)

        self.gat("a moeda da ponta fica para trás")
        self.play(Flash(p_m2_15, color=ACC, line_length=0.22, flash_radius=0.28), run_time=0.7)

        self.gat("um décimo e meio de segundo")
        lupa = zoom_inset(P3(4.55, -0.35), w=3.2, h=2.05, folga_cm=NUM["folga_015_cm"], th=th_15)
        tit_lupa = txt("ZOOM ×3 · t = 0,15 s", 24, color=GEO).next_to(lupa, UP, buff=0.16)
        val_folga = nm(r"5{,}4\ \mathrm{cm}", GEO, 38).next_to(lupa, DOWN, buff=0.16)
        chamada_lupa = DashedLine(p_pt_15 + 0.12 * RIGHT, lupa.get_left() + 0.1 * UP, dash_length=0.09).set_stroke(GEO, 2.0, opacity=0.75)
        self.play(FadeIn(lupa), FadeIn(tit_lupa), Create(chamada_lupa), FadeIn(val_folga), run_time=0.9)

        self.gat("caindo em queda livre")
        s_g = seta(p_m2_15 + P3(0.28, 0.0), p_m2_15 + P3(0.28, -1.10), ACC, 6, tip=0.20)
        lbl_g = T("g", 40, ACC).next_to(s_g, RIGHT, buff=0.22)
        self.play(FadeIn(s_g), FadeIn(lbl_g), run_time=0.7)

        self.gat("então a ponta da régua está descendo mais depressa")
        s_ponta = seta(p_pt_15 + P3(0.0, -0.06), p_pt_15 + P3(0.0, -1.71), ACC, 6, tip=0.22)
        lbl_ponta = T(r"\tfrac{3}{2}g", 40, ACC).next_to(s_ponta, LEFT, buff=0.20)
        s_meio = seta(p_m1_15 + P3(0.0, -0.08), p_m1_15 + P3(0.0, -0.90), ACC, 6, tip=0.18)
        lbl_meio = VGroup(nm("0{,}75", ACC, 36), T("g", 36, ACC)).arrange(RIGHT, buff=0.06).next_to(s_meio, LEFT, buff=0.20)
        self.play(FadeIn(s_ponta), FadeIn(lbl_ponta), FadeIn(s_meio), FadeIn(lbl_meio), run_time=0.9)
        self.foco = lupa
        self.ate(0.99)

        # ── H3: a pergunta central e a apresentação do TORQUE (τ) ──
        self.an("H3")
        self.sem_selo()
        self.play(FadeOut(tag_meio), FadeOut(lupa), FadeOut(tit_lupa), FadeOut(chamada_lupa), FadeOut(val_folga), run_time=0.4)

        perg = VGroup(
            txt("SÓ O PRÓPRIO PESO ATUA:", 24, color=GEO),
            txt("COMO A PONTA ACELERA MAIS QUE g ?", 26, bold=True, color=ACC),
        ).arrange(DOWN, buff=0.14).move_to(P3(3.45, 1.55))
        self.play(FadeIn(perg, shift=0.1 * DOWN), run_time=0.8)

        self.gat("acelerar mais do que a gravidade")
        self.play(
            lbl_ponta.animate.scale(1.18),
            lbl_g.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.gat("uma grandeza nova")
        arco_h = arco_torque(p_dob, r=0.58, sentido=-1, a0=0.1, amp=1.6, cor=TQ)
        card_tau = RoundedRectangle(width=4.4, height=1.35, corner_radius=0.16).move_to(P3(3.55, -0.55))
        card_tau.set_fill(PANEL, 0.92).set_stroke(TQ, 2.8)
        card_tau._fundo = card_tau._caixa = True
        txt_tau = VGroup(txt("TORQUE", 34, bold=True, color=TQ), T(r"\tau", 54, TQ)).arrange(RIGHT, buff=0.35).move_to(card_tau.get_center())
        self.play(FadeIn(arco_h), Create(card_tau), FadeIn(txt_tau, shift=0.1 * UP), run_time=0.8)
        self.foco = txt_tau
        self.ate(0.99)
