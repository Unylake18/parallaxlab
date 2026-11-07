"""Lote PT6: T6 — QUANDO NADA ACELERA: EQUILÍBRIO.
T6-1: disco horizontal visto de cima (sem gravidade no plano do giro) com furo excêntrico girando a ω constante (α = 0). O CM descreve um
círculo tracejado, logo a_cm ≠ 0 e o eixo aplica força Σ F⃗ = M a⃗_cm apontando do CM para o eixo (girando junto): α = 0 ⇒ Σ τ_z = 0, MAS Σ F⃗ ≠ 0⃗.
T6-2: equilíbrio estático (Σ F⃗ = 0⃗ e Σ τ⃗ = 0⃗ em caixa PANEL); inset mostrando a régua recém-largada (ω = 0, α ≠ 0: PARADA NUM INSTANTE ≠ EQUILÍBRIO);
mudança de ponto τ⃗_{P'} = τ⃗_P + (r⃗_P − r⃗_{P'}) × Σ F⃗ com o termo extra indo a zero quando Σ F⃗ = 0⃗.
T6-3: gangorra 2,5D com 30 kg a 1,5 m e 45 kg a 1,0 m (30·g·1,5 = 45·g·1,0, g riscado) e N = (30 + 45) g ≈ 735 N.
T6-4: régua segurada na horizontal (M g / 2 na dobradiça e M g / 2 no dedo) vs instante logo após soltar (M g / 4 na dobradiça)."""
from pecas22 import *  # noqa: F401,F403


class LoteT6(Lote22):
    def corpo(self):
        self.secao("QUANDO NADA ACELERA: EQUILÍBRIO")

        # ── T6-1: disco horizontal furado fora do centro girando a ω constante (α = 0 ⇒ Σ τ_z = 0, MAS Σ F⃗ ≠ 0⃗) ──
        self.an("T6-1")
        C_DF = P3(-3.8, -0.45)
        R_DF = 1.85
        ang_df = ValueTracker(0.35)
        ang_df.add_updater(lambda m, dt: m.increment_value(1.25 * dt))
        self.add(ang_df)

        def _cena_df():
            a = ang_df.get_value()
            df = disco_furado(C_DF, R=R_DF, ang=a)
            # Seta de aceleração centrípeta do CM apontando do CM para o eixo C_DF e força do mancal na mesma direção
            u_in = vet_unit(C_DF - df.cm)
            s_acm = seta(df.cm, df.cm + u_in * 0.72, ACC, 5, tip=0.17, z=18)
            s_feixo = seta(C_DF - u_in * 0.65, C_DF + u_in * 0.55, FC, 6, tip=0.19, z=19)
            return VGroup(df, s_acm, s_feixo)

        v_df = vivo(_cena_df)
        a_om = seta_curva(C_DF, R_DF + 0.34, 1.8, 0.85, VEL, 5.5)
        l_om = VGroup(T(r"\omega = \mathrm{const}", 36, VEL), T(r"\alpha = 0", 36, ACC)).arrange(DOWN, buff=0.08).move_to(C_DF + P3(0.0, 2.55))
        tag_mesa = txt("VISTA DE TOPO · MESA HORIZONTAL", 28, color=GEO).move_to(C_DF + P3(0.0, -2.55))

        A1, ia1 = M(r"\alpha = 0", r"\ \Rightarrow\ ", r"\sum", r"\tau_z", "=", "0", size=50)
        cab61 = txt("GIRO UNIFORME:", 26, bold=True, color=TQ)
        self.pilha.poe(cab61)
        self.play(FadeIn(v_df), FadeIn(tag_mesa), FadeIn(cab61), run_time=0.8)
        self.pilha.poe(A1)
        self.gat("pensa num disco deitado")
        self.play(FadeIn(a_om), run_time=0.5)
        self.gat("com velocidade angular constante")
        self.play(FadeIn(l_om), run_time=0.5)
        self.gat("a aceleração angular é zero")
        self.monta(A1, ia1, {0: l_om[1]}, rt=1.0)

        A2, ia2 = M(r"\vec a_{\mathrm{cm}} \neq \vec 0", r"\ \Rightarrow\ ", r"\sum", r"\vec F", "=", "M", r"\vec a_{\mathrm{cm}}", size=46)
        self.pilha.poe(A2)
        self.gat("ele tem aceleração centrípeta")
        self.monta(A2, ia2, {}, rt=1.1)

        linha_mas = VGroup(
            txt("MAS", 24, bold=True, color=FC),
            M(r"\sum\vec F \neq \vec 0", size=46)[0],
            txt("(MANCAL)", 28, bold=True, color=FC),
        ).arrange(RIGHT, buff=0.14)
        A3 = VGroup(
            M(r"\alpha = 0 \ \Rightarrow\ \sum\tau_z = 0", size=46)[0],
            linha_mas,
        ).arrange(DOWN, buff=0.14)
        A3b = caixa_l(A3, FC)
        self.pilha.poe(A3b)
        self.gat("então girar com velocidade angular constante")
        self.play(Create(A3b[0]), FadeIn(A3, shift=0.08 * UP), run_time=0.8)
        self.foco = A3b
        self.ate(0.99)

        # ── T6-2: equilíbrio estático (Σ F⃗ = 0⃗ e Σ τ⃗ = 0⃗), inset PARADA NUM INSTANTE ≠ EQUILÍBRIO e escolha livre do ponto P' ──
        self.an("T6-2")
        pe63 = self.poeira_extra(n=130, seed=13, vmul=2.4, opm=1.8)      # gangorra parada por ~15 s: poeira mais viva (PARADO)
        v_df.clear_updaters()
        ang_df.clear_updaters()
        self.pilha.limpa()
        self.play(FadeOut(VGroup(v_df, a_om, l_om, tag_mesa, A1, A2, A3b)), run_time=0.45)

        # Inset na esquerda: régua recém-largada com ω = 0 mas α ≠ 0 (PARADA NUM INSTANTE ≠ EQUILÍBRIO)
        cx_in = RoundedRectangle(width=7.0, height=3.0, corner_radius=0.16).move_to(P3(-3.85, 1.0))
        cx_in.set_fill(PANEL, 0.88).set_stroke(ACC, 2.4)
        cx_in._fundo = True
        r_in = regua2d(P3(-5.8, 1.95), comp=3.4, esp=0.18, ang=0.0, bancada=False)
        s_in = seta(r_in.cm, r_in.cm + DOWN * 0.52, FC, 5, tip=0.16)
        a_in = arco_torque(r_in.dob, r=0.42, sentido=-1, a0=0.1, amp=1.5, cor=ACC, w=4.5)
        txt_in1 = VGroup(T(r"\omega = 0", 36, VEL), txt("MAS", 28), T(r"\alpha \neq 0", 36, ACC)).arrange(RIGHT, buff=0.18).move_to(P3(-3.8, 0.72))
        txt_in2 = txt("PARADA NUM INSTANTE ≠ EQUILÍBRIO", 26, bold=True, color=ACC).move_to(P3(-3.8, 0.12))
        g_inset = VGroup(cx_in, r_in, s_in, a_in, txt_in1, txt_in2)

        # Caixa PANEL com as duas condições do equilíbrio estático na Pilha
        B1, ib1 = M(r"\sum", r"\vec F", "=", r"\vec 0", r"\quad\text{E}\quad", r"\sum", r"\vec\tau", "=", r"\vec 0", size=52)
        B1b = caixa_l(B1, TQ)
        cab62 = txt("CONDIÇÕES DE EQUILÍBRIO:", 26, bold=True, color=TQ)
        self.pilha.poe(cab62)
        self.play(FadeIn(VGroup(cx_in, r_in)), FadeIn(cab62), run_time=0.7)
        self.pilha.poe(B1b)
        self.gat("o corpo continua parado")
        self.selo("EQUILÍBRIO ESTÁTICO", "= CONTINUA PARADO")
        self.gat("zero num instante")
        self.play(FadeIn(VGroup(s_in, a_in, txt_in1, txt_in2), shift=0.1 * UP), run_time=0.6)
        self.gat("a força resultante e o torque resultante")
        self.cx(B1b[0])
        self.monta(B1, ib1, {}, rt=1.1)

        # Esquema inferior na esquerda mostrando dois pontos P e P' e a relação entre τ_{P'} e τ_P
        p_P = P3(-5.4, -1.65)
        p_P2 = P3(-2.4, -1.65)
        dP = Dot(p_P, radius=0.08, color=TQ)
        dP2 = Dot(p_P2, radius=0.08, color=VETC)
        s_dP = seta(p_P2, p_P, VETC, 5, tip=0.18)
        l_P = T("P", 36, TQ).next_to(dP, DOWN, buff=0.14)
        l_P2 = T("P'", 36, VETC).next_to(dP2, DOWN, buff=0.14)
        l_dr = T(r"\Delta\vec r = \vec r_P - \vec r_{P'}", 36, VETC).next_to(s_dP, UP, buff=0.14)
        g_pts = VGroup(dP, dP2, s_dP, l_P, l_P2, l_dr)

        self.gat("não depende do ponto")
        self.play(FadeIn(g_pts), run_time=0.7)

        B2a, ib2a = M(r"\sum\vec\tau_{P'}", "=", r"\sum\vec\tau_P", size=46)
        B2b, ib2b = M("+", r"\Delta\vec r", r"\times", r"\sum\vec F", size=46)
        B2 = VGroup(B2a, B2b)
        self.pilha.poe(B2a)
        self.pilha.poe(B2b, dx=0.5)
        self.monta(B2a, ib2a, {}, rt=0.8)
        self.gat("aparece um termo extra")
        self.monta(B2b, ib2b, {1: l_dr}, rt=1.1)

        # Risca Σ F⃗ indo a zero → Σ τ_{P'} = Σ τ_P = 0
        self.gat("termo extra zero")
        risco_sf = Line(mp(B2b, ib2b, [1, 2, 3]).get_corner(DL), mp(B2b, ib2b, [1, 2, 3]).get_corner(UR)).set_stroke(MAS, 3.8)
        risco_sf._risco = True
        z_sf = T(r"\vec 0", 38, MAS).next_to(mp(B2b, ib2b, [3]), RIGHT, buff=0.22)
        self.play(Create(risco_sf), FadeIn(z_sf), run_time=0.6)

        B3, ib3 = M(r"\sum\vec\tau_{P'}", "=", r"\sum\vec\tau_P", "=", r"\vec 0", size=50)
        self.pilha.poe(B3)
        self.monta(B3, ib3, {0: mp(B2a, ib2a, [0]), 2: mp(B2a, ib2a, [2])}, rt=0.9)
        self.selo("ATALHO", "ESCOLHA O PONTO DA FORÇA DESCONHECIDA: BRAÇO ZERO")
        self.foco = B3
        self.ate(0.99)

        # ── T6-3: gangorra 2,5D em equilíbrio (30 kg a 1,5 m vs 45 kg a 1,0 m; N = 735 N) ──
        self.an("T6-3")
        self.sem_selo()
        self.pilha.limpa()
        self.play(FadeOut(VGroup(g_inset, g_pts, B1b, B2, risco_sf, z_sf, B3)), run_time=0.45)

        P_PIV = P3(-3.7, -1.0)
        gan = gangorra(P_PIV, escala=1.0, ang=0.0)
        l_30 = nm(r"30\ \mathrm{kg}", MAS, 36).next_to(gan.c30, UP, buff=0.36)
        l_45 = nm(r"45\ \mathrm{kg}", MAS, 36).next_to(gan.c45, UP, buff=0.42)
        cota_15 = nm(r"1{,}5\ \mathrm{m}", GEO, 36).move_to((P_PIV + gan.p30) / 2 + DOWN * 1.12)
        cota_10 = nm(r"1{,}0\ \mathrm{m}", GEO, 36).move_to((P_PIV + gan.p45) / 2 + DOWN * 1.12)
        s_p30 = seta(gan.p30, gan.p30 + DOWN * 1.05, FC, 5.5, tip=0.18)
        s_p45 = seta(gan.p45, gan.p45 + DOWN * 1.45, FC, 5.5, tip=0.18)
        s_N = seta(P_PIV + DOWN * 0.65, P_PIV + UP * 1.65, FC, 6.5, tip=0.22)
        l_N = T("N", 38, FC).next_to(P_PIV + UP * 1.65, UP, buff=0.14)

        C1, ic1 = M("30", "g", r"\cdot", "1{,}5", "-", "45", "g", r"\cdot", "1{,}0", "=", "0", size=46)
        cab63 = txt("GANGORRA EM EQUILÍBRIO:", 26, bold=True, color=TQ)
        self.pilha.poe(cab63)
        self.play(FadeIn(gan), FadeIn(cab63), run_time=0.7)
        self.pilha.poe(C1)
        self.gat("na gangorra")
        self.play(FadeIn(s_p30), FadeIn(s_p45), run_time=0.8)
        self.gat("pega o próprio apoio")
        self.play(FadeIn(s_N), FadeIn(l_N), run_time=0.6)
        self.gat("uma massa de trinta quilos")
        self.play(FadeIn(l_30), FadeIn(cota_15), run_time=0.6)
        self.gat("quarenta e cinco a um metro")
        self.play(FadeIn(l_45), FadeIn(cota_10), run_time=0.6)
        self.gat("porque trinta vezes um e meio")
        self.monta(C1, ic1, {0: l_30, 3: cota_15, 5: l_45, 8: cota_10}, rt=1.1)

        # Risca g nos dois termos
        rg1 = Line(mp(C1, ic1, [1]).get_corner(DL), mp(C1, ic1, [1]).get_corner(UR)).set_stroke(MAS, 3.6)
        rg1._risco = True
        rg2 = Line(mp(C1, ic1, [6]).get_corner(DL), mp(C1, ic1, [6]).get_corner(UR)).set_stroke(MAS, 3.6)
        rg2._risco = True
        self.play(Create(rg1), Create(rg2), run_time=0.5)

        C2, ic2 = M("45", "=", "45", r"\quad(\tau = 441\,\mathrm{N\cdot m})", size=46)
        self.pilha.poe(C2)
        self.gat("quarenta e cinco vezes um")
        self.monta(C2, ic2, {}, rt=0.7)

        C3, ic3 = M("N", "=", "(30 + 45)", "g", "=", "735", r"\,\mathrm{N}", size=46)
        self.pilha.poe(C3)
        self.gat("setecentos e trinta e cinco newtons")
        self.monta(C3, ic3, {0: l_N}, rt=1.1)
        self.foco = C3
        self.ate(0.99)

        # ── T6-4: régua segurada na horizontal (M g / 2 + M g / 2) vs instante logo após soltar (M g / 4 na dobradiça) ──
        self.an("T6-4")
        self.remove(pe63)
        self.pilha.limpa()
        self.play(FadeOut(VGroup(gan, l_30, l_45, cota_15, cota_10, s_p30, s_p45, s_N, l_N, C1, rg1, rg2, C2, C3)), run_time=0.45)

        # Esquema duplo na esquerda: em cima (SEGURADA: EQUILÍBRIO), embaixo (SOLTA: ACELERANDO)
        P_SUP = P3(-5.8, 0.75)
        L_R6 = 4.4
        r_sup = regua2d(P_SUP, comp=L_R6, esp=0.22, ang=0.0, bancada=True)
        dedo6 = dedo_silhueta(r_sup.ponta + DOWN * 0.08, dir_dedo=UP, comp=0.80)
        s_mg_sup = seta(r_sup.cm, r_sup.cm + DOWN * 1.20, FC, 5.5, tip=0.19)
        l_mg_sup = T("Mg", 36, FC).next_to(s_mg_sup, RIGHT, buff=0.12)
        s_dob_sup = seta(r_sup.dob, r_sup.dob + UP * 0.65, FC, 5.5, tip=0.18)
        l_dob_sup = T(r"\tfrac{1}{2}Mg", 36, FC).next_to(s_dob_sup, UP, buff=0.10)
        s_ded_sup = seta(r_sup.ponta, r_sup.ponta + UP * 0.65, FC, 5.5, tip=0.18)
        l_ded_sup = T(r"\tfrac{1}{2}Mg", 36, FC).next_to(s_ded_sup, UP, buff=0.10)
        g_sup = VGroup(r_sup, dedo6, s_mg_sup, l_mg_sup, s_dob_sup, l_dob_sup, s_ded_sup, l_ded_sup)

        cab64 = txt("RÉGUA SEGURADA × SOLTA:", 26, bold=True, color=TQ)
        self.pilha.poe(cab64)
        self.play(FadeIn(VGroup(r_sup, dedo6)), FadeIn(cab64), run_time=0.7)
        self.gat("segura a ponta")
        self.play(FadeIn(VGroup(s_mg_sup, l_mg_sup, s_dob_sup, l_dob_sup, s_ded_sup, l_ded_sup)), run_time=0.8)

        D1, id1 = M(r"F_{\mathrm{dob}}", "=", r"F_{\mathrm{dedo}}", "=", r"\frac{1}{2}", "M", "g", size=48)
        self.pilha.poe(D1)
        self.gat("o dedo segura metade do peso")
        self.monta(D1, id1, {0: l_dob_sup, 2: l_ded_sup}, rt=1.0)

        # Embaixo: régua logo após soltar (F_dedo = 0, a_cm = 3g/4 para baixo ⇒ F_dob = M g / 4)
        P_INF = P3(-5.8, -1.75)
        r_inf = regua2d(P_INF, comp=L_R6, esp=0.22, ang=-0.05, bancada=True)
        s_mg_inf = seta(r_inf.cm, r_inf.cm + DOWN * 1.20, FC, 5.5, tip=0.19)
        s_acm_inf = seta(r_inf.cm + RIGHT * 0.45, r_inf.cm + RIGHT * 0.45 + DOWN * 0.90, ACC, 5.5, tip=0.18)
        l_acm_inf = T(r"a_{\mathrm{cm}} = \tfrac{3}{4}g", 38, ACC).move_to(r_inf.cm + P3(0.45, -0.90) + P3(1.35, 0.0))
        s_dob_inf = seta(r_inf.dob, r_inf.dob + UP * 0.40, FC, 5.5, tip=0.17)
        l_dob_inf = T(r"\tfrac{1}{4}Mg", 40, FC).next_to(s_dob_inf, UP, buff=0.08)
        g_inf = VGroup(r_inf, s_mg_inf)
        g_acm = VGroup(s_acm_inf, l_acm_inf)
        g_dobinf = VGroup(s_dob_inf, l_dob_inf)

        self.gat("no instante em que o dedo sai")
        self.play(FadeIn(g_inf), run_time=0.8)

        D2, id2 = M("M", "g", "-", r"F_{\mathrm{dob}}", "=", "M", r"a_{\mathrm{cm}}", "=", "M", r"\frac{3}{4}", "g", size=46)
        self.pilha.poe(D2)
        self.gat("o centro de massa passa a acelerar")
        self.play(FadeIn(g_acm), run_time=0.6)
        self.gat("o peso menos a força da dobradiça")
        self.monta(D2, id2, {6: l_acm_inf}, rt=1.0)

        D3, id3 = M(r"F_{\mathrm{dob}}", "=", r"\frac{1}{4}", "M", "g", size=52)
        D3b = caixa_l(D3, FC)
        self.pilha.poe(D3b)
        self.gat("só um quarto do peso")
        self.cx(D3b[0])
        self.play(FadeIn(g_dobinf), run_time=0.5)
        self.monta(D3, id3, {0: l_dob_inf}, rt=1.0)
        self.foco = D3b
        self.ate(0.99)
