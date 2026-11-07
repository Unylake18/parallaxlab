"""Lote PH: hook H1–H3 (Three.js 'regua'). Régua metálica de 1,0 m presa numa dobradiça horizontal na beira da bancada, com duas moedas
sobre ela (meio a 50 cm e ponta a 100 cm). A câmera começa a 3/4, desce até a vista frontal pura e PARA antes de qualquer seta ou cota.
Em H2, queda em câmera lenta ×10 de t = 0 até t = 0,15 s (θ = 9,5°, folga de 5,4 cm na ponta em lupa ×3; moeda do meio segue colada,
iniciando escorregamento em ~2,9° com N > 0). Setas verdes de aceleração comparam g, 3g/2 e 0,75g. Em H3, a pergunta central apresenta o TORQUE (τ)."""
from pecas22 import *  # noqa: F401,F403


class LoteHook(Lote22):
    def corpo(self):
        t_fis = ValueTracker(0.0)
        u_cam = ValueTracker(0.0)
        dedo_tr = ValueTracker(1.0)                       # D1: dedo 3D (Three.js) apoiado na ponta até "tirar o dedo"
        self.add(t_fis, u_cam, dedo_tr)

        def est(t):
            tf = min(0.15, max(0.0, t_fis.get_value()))
            cam = cam_hook(u_cam.get_value())
            e = estado_regua(tf, dedo=dedo_tr.get_value())
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

        # ── H1: dolly-in lento de 3/4 até a frontal (a régua ocupa ≥ 70% da largura); a câmera PARA antes de qualquer cota ──
        self.an("H1")
        self.play(u_cam.animate.set_value(1.0), run_time=9.0, rate_func=lambda t: 0.35 * smooth(t) + 0.65 * t)
        cam_f = cam_hook(1.0)
        p_dob = P3(*tela_regua(cam_f, 0.0, 0.0), 0.0)
        p_meio = P3(*tela_regua(cam_f, 0.50, 0.0), 0.0)
        p_ponta = P3(*tela_regua(cam_f, 1.00, 0.0), 0.0)

        # Cota L = 1,0 m abaixo da régua, destaque da dobradiça (rótulo afastado, com chamada) e o dedo na ponta
        cota_L = VGroup(
            Line(p_dob + 0.60 * DOWN, p_ponta + 0.60 * DOWN).set_stroke(TQ, 3.2),
            Line(p_dob + 0.46 * DOWN, p_dob + 0.74 * DOWN).set_stroke(TQ, 3.2),
            Line(p_ponta + 0.46 * DOWN, p_ponta + 0.74 * DOWN).set_stroke(TQ, 3.2),
            VGroup(MathTex("L=", font_size=48, color=GEO), nm(r"1{,}0\ \mathrm{m}", GEO, 48)).arrange(RIGHT, buff=0.1).move_to((p_dob + p_ponta) / 2 + 1.15 * DOWN),
        ).set_z_index(12)
        anel_dob = Circle(radius=0.30).move_to(p_dob).set_stroke(TQ, 3.4)
        lbl_dob = txt("DOBRADIÇA", 32, bold=True, color=TQ).move_to(p_dob + P3(1.45, 1.55))
        ch_dob = Line(p_dob + 0.30 * UR, lbl_dob.get_bottom() + 0.25 * DOWN + 0.55 * LEFT).set_stroke(TQ, 2.2)
        self.play(FadeIn(cota_L), FadeIn(anel_dob), FadeIn(lbl_dob), Create(ch_dob), run_time=0.9)

        self.gat("duas moedas")
        lbl_m2 = txt("MOEDA NA PONTA", 32, bold=True, color=ACC).move_to(p_ponta + P3(1.4, 1.05))
        lbl_m1 = txt("MOEDA NO MEIO", 32, bold=True, color=ACC).move_to(p_meio + P3(0.0, 1.05))
        ch_m2 = Line(lbl_m2.get_bottom() + 0.24 * DOWN, p_ponta + P3(0.0, 0.45)).set_stroke(ACC, 2.2)
        ch_m1 = Line(lbl_m1.get_bottom() + 0.24 * DOWN, p_meio + P3(0.0, 0.45)).set_stroke(ACC, 2.2)
        self.play(FadeIn(lbl_m2, shift=0.1 * DOWN), FadeIn(lbl_m1, shift=0.1 * DOWN), Create(ch_m2), Create(ch_m1), run_time=0.7)

        self.gat("tirar o dedo")
        self.play(dedo_tr.animate.set_value(0.0), FadeOut(cota_L), run_time=0.6)

        self.gat("as moedas vão junto")
        self.selo("PERGUNTA", "AS MOEDAS DESCEM JUNTO COM A RÉGUA?")
        anel1 = Circle(radius=0.40).move_to(p_meio + 0.18 * UP).set_stroke(ACC, 3.2)
        anel2 = Circle(radius=0.40).move_to(p_ponta + 0.18 * UP).set_stroke(ACC, 3.2)
        self.play(FadeIn(anel1), FadeIn(anel2), run_time=0.4)
        self.play(anel1.animate.scale(1.22), anel2.animate.scale(1.22), rate_func=there_and_back, run_time=0.9)
        self.play(FadeOut(anel1), FadeOut(anel2), FadeOut(anel_dob), FadeOut(lbl_dob), FadeOut(ch_dob), FadeOut(lbl_m1), FadeOut(lbl_m2),
                  FadeOut(ch_m1), FadeOut(ch_m2), run_time=0.4)
        self.foco = f3
        self.ate(0.99)

        # ── H2: largada em câmera lenta ×10 (0 → 0,15 s), rastro estroboscópico, lupa ×3 na ponta (5,4 cm) e setas de aceleração ──
        self.an("H2")
        self.selo("CÂMERA LENTA", [["QUEDA DE", nm("0", GEO, 36), "A", nm(r"0{,}15\ \mathrm{s}", GEO, 36)]])
        th_15 = float(TAB_REGUA["th"][1500])
        # rastro estroboscópico: cópias fantasma da régua a cada 0,025 s (0 → 0,15 s) e pontos das duas moedas
        idxs = [int(round(0.025 * k / 1e-4)) for k in range(1, 7)]
        fant = VGroup(*[
            Line(P3(*tela_regua(cam_f, 0.0, float(TAB_REGUA["th"][i])), 0.0), P3(*tela_regua(cam_f, 1.0, float(TAB_REGUA["th"][i])), 0.0)).set_stroke(TQ, 2.2, opacity=0.2 + 0.05 * k).set_z_index(5)
            for k, i in enumerate(idxs, 1)])
        pt_m2 = VGroup(*[Dot(P3(*projeta3d(cam_f, (float(TAB_REGUA["m2x"][i]), 0.0, float(TAB_REGUA["m2z"][i]))), 0.0), radius=0.05, color=ACC).set_z_index(13) for i in idxs])
        pt_m1 = VGroup(*[Dot(P3(*projeta3d(cam_f, (float(TAB_REGUA["m1x"][i]), 0.0, float(TAB_REGUA["m1z"][i]))), 0.0), radius=0.05, color=ACC).set_z_index(13) for i in idxs])
        self.play(t_fis.animate.set_value(0.15), LaggedStart(*[FadeIn(f_) for f_ in fant], lag_ratio=0.8), LaggedStart(*[FadeIn(d_) for d_ in pt_m2], lag_ratio=0.8),
                  LaggedStart(*[FadeIn(d_) for d_ in pt_m1], lag_ratio=0.8), run_time=3.2, rate_func=linear)

        p_m1_15 = P3(*projeta3d(cam_f, (float(TAB_REGUA["m1x"][1500]), 0.0, float(TAB_REGUA["m1z"][1500]))), 0.0)
        p_m2_15 = P3(*projeta3d(cam_f, (float(TAB_REGUA["m2x"][1500]), 0.0, float(TAB_REGUA["m2z"][1500]))), 0.0)
        p_pt_15 = P3(*tela_regua(cam_f, 1.0, th_15), 0.0)

        tag_meio = txt("SEGUE ENCOSTADA", 30, bold=True, color=ACC).move_to(p_m1_15 + P3(-0.3, 1.7))
        self.play(FadeIn(tag_meio, shift=0.08 * DOWN), run_time=0.6)

        self.gat("a moeda da ponta fica para trás")
        self.play(Flash(p_m2_15, color=ACC, line_length=0.30, flash_radius=0.40), run_time=0.7)

        self.gat("um décimo e meio de segundo")
        lupa = zoom_inset(P3(6.4, -0.1), w=2.9, h=1.9, folga_cm=NUM["folga_015_cm"], th=th_15)
        tit_lupa = VGroup(txt("ZOOM ×3", 30, color=GEO), linha_base([T("t", 46, GEO), nm(r"=\ 0{,}15\ \mathrm{s}", GEO, 46)], 0.1)).arrange(DOWN, buff=0.08).next_to(lupa, UP, buff=0.3)
        val_folga = nm(r"5{,}4\ \mathrm{cm}", GEO, 44).move_to(lupa.get_center() + P3(0.0, -1.45))
        chamada_lupa = DashedLine(p_pt_15 + 0.10 * UP + 0.14 * RIGHT, lupa.get_left() + 0.1 * DOWN, dash_length=0.09).set_stroke(GEO, 2.0, opacity=0.75)
        self.play(FadeIn(lupa), FadeIn(tit_lupa), Create(chamada_lupa), FadeIn(val_folga), run_time=0.9)

        self.gat("caindo em queda livre")
        s_g = seta(p_m2_15 + P3(0.45, -0.30), p_m2_15 + P3(0.45, -1.20), ACC, 6, tip=0.20)
        lbl_g = T("g", 44, ACC).next_to(s_g, RIGHT, buff=0.20)
        self.play(FadeIn(s_g), FadeIn(lbl_g), run_time=0.7)

        self.gat("então a ponta da régua está descendo mais depressa")
        s_ponta = seta(p_pt_15 + P3(-0.05, -0.30), p_pt_15 + P3(-0.05, -1.80), ACC, 6, tip=0.22)
        lbl_ponta = T(r"\tfrac{3}{2}g", 46, ACC).next_to(s_ponta, LEFT, buff=0.20)
        s_meio = seta(p_m1_15 + P3(0.0, -0.30), p_m1_15 + P3(0.0, -1.00), ACC, 6, tip=0.18)
        lbl_meio = VGroup(nm("0{,}75", ACC, 42), T("g", 42, ACC)).arrange(RIGHT, buff=0.06).next_to(s_meio, LEFT, buff=0.20)
        self.play(FadeIn(s_ponta), FadeIn(lbl_ponta), FadeIn(s_meio), FadeIn(lbl_meio), run_time=0.9)
        self.foco = lupa
        self.ate(0.99)

        # ── H3: a pergunta central (g em MathTex) e a apresentação do TORQUE (τ) ──
        self.an("H3")
        self.sem_selo()
        self.play(FadeOut(tag_meio), FadeOut(lupa), FadeOut(tit_lupa), FadeOut(chamada_lupa), FadeOut(val_folga), run_time=0.4)

        perg = VGroup(
            txt("SÓ O PESO E A DOBRADIÇA ATUAM:", 32, color=GEO),
            linha_base([txt("COMO A PONTA ACELERA MAIS QUE", 36, bold=True, color=ACC), T("g", 46, ACC), txt("?", 36, bold=True, color=ACC)], 0.24),
        ).arrange(DOWN, buff=0.16).move_to(P3(-3.0, 1.7))
        self.play(FadeIn(perg, shift=0.1 * DOWN), run_time=0.8)

        self.gat("nas hipóteses")
        self.selo("HIPÓTESES", "RÉGUA UNIFORME · MOEDAS LEVES · DOBRADIÇA SEM ATRITO")
        self.gat("acelerar mais que a gravidade")
        self.play(
            lbl_ponta.animate.scale(1.18),
            lbl_g.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.gat("numa grandeza nova")
        arco_h = arco_torque(p_dob, r=0.62, sentido=-1, a0=0.1, amp=1.6, cor=TQ)
        card_tau = RoundedRectangle(width=4.6, height=1.45, corner_radius=0.16).move_to(P3(5.3, -3.35))
        card_tau.set_fill(PANEL, 0.92).set_stroke(TQ, 2.8)
        card_tau._fundo = card_tau._caixa = True
        txt_tau = VGroup(txt("TORQUE", 38, bold=True, color=TQ), T(r"\tau", 60, TQ)).arrange(RIGHT, buff=0.35).move_to(card_tau.get_center())
        self.play(FadeIn(arco_h), Create(card_tau), FadeIn(txt_tau, shift=0.1 * UP), run_time=0.8)
        self.foco = txt_tau
        self.ate(0.99)
