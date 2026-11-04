"""Lote PT4: T4 — DE VOLTA À RÉGUA: ONDE A PONTA PASSA DE g.
T4-1: Three.js 'regua' frontal transiciona para o esquema 2D limpo na metade esquerda. O peso distribuído equivale a M g atuando no CM (L/2):
τ_peso = Σ m_i g x_i = g Σ m_i x_i = M g x_cm.
T4-2: τ_z = −M g (L/2), I = ⅓ M L² → α_z = −3g / (2L) com M riscado (TransformByGlyphMap). Selo 'O SINAL DIZ: GIRA NO HORÁRIO', |α| = 14,7 rad/s².
T4-3: selo 'NO INSTANTE DA LARGADA: ω = 0 ⇒ a_c = 0' com a_c = ω² r riscado. Reta inclinada a_t(r) = |α| r = (3g / 2L) r cruzando a linha
tracejada de g em r = 2L/3 ≈ 67 cm; ponta com 3g/2 = 14,7 m/s², moeda do meio em 50 cm (0,75g < g) e moeda da ponta em 100 cm (queda livre g).
T4-4: régua fatiada em N = 12 fatias com setas azuis da RESULTANTE DAS FORÇAS ALÉM DO PESO m_i(|α| r_i − g) = m_i g (3 r_i / 2L − 1).
Na fatia colada à dobradiça, a seta se divide em VIZINHOS + DOBRADIÇA; os pares internos somam zero e sobra DOBRADIÇA: M g / 4 PARA CIMA.
Selo 'NÃO HÁ NADA VIOLANDO A GRAVIDADE'.
T4-5: vassoura (L = 1,2 m) vs lápis (L = 0,15 m) tombando da vertical com RK4 de θ̈ = (3g / 2L) sen θ e relógios marcando a razão √8 ≈ 2,8."""
from pecas22 import *  # noqa: F401,F403


class LoteT4(Lote22):
    def corpo(self):
        cam = cam_regua_frente(K=4.8, xc=-3.6, yc=0.55, camx=0.45, camz=-0.04)

        def est(t):
            e = estado_regua(0.0, moedas=False)
            e["cam"] = cam
            if not PEDIDOS3D:
                self.reg(
                    "t4_regua",
                    dobradica=tela_regua(cam, 0.0, 0.0),
                    cm=tela_regua(cam, 0.50, 0.0),
                    dois_tercos=tela_regua(cam, 2.0 / 3.0, 0.0),
                    ponta=tela_regua(cam, 1.00, 0.0),
                )
            return r4(e)

        f3 = Fundo3D(self, "regua", est)
        self.add(f3)
        self.f3 = f3
        self.secao("DE VOLTA À RÉGUA")

        # ── T4-1: Three.js 'regua' frontal → esquema 2D limpo + peso no CM (τ_peso = M g x_cm) ──
        self.an("T4-1")
        A0_t4 = txt("TORQUE DO PESO DISTRIBUÍDO:", 26, bold=True, color=TQ)
        self.pilha.poe(A0_t4)
        self.play(FadeIn(A0_t4), run_time=0.6)
        self.wait(0.6)
        # Transição limpa para o esquema 2D da régua na metade esquerda
        P_DOB = P3(-6.0, 0.65)
        L_ESQ = 4.8
        reg = regua2d(P_DOB, comp=L_ESQ, esp=0.24, ang=0.0, n_fatias=0, bancada=True)
        self.play(f3.op.animate.set_value(0.0), FadeIn(reg), run_time=0.8)

        # Setinhas do peso distribuído m_i g ao longo da régua que se juntam em M g no CM
        setas_p = VGroup(*[
            seta(P_DOB + RIGHT * (L_ESQ * (k + 0.5) / 8.0), P_DOB + RIGHT * (L_ESQ * (k + 0.5) / 8.0) + DOWN * 0.62, FC, 3.8, tip=0.14, op=0.65)
            for k in range(8)
        ])
        self.gat("cada pedacinho tem o seu peso")
        self.play(FadeIn(setas_p), run_time=0.7)

        A1, ia1 = M(r"\tau_{\mathrm{peso}}", "=", r"\sum", "m_i", "g", "x_i", "=", "g", r"\sum", "m_i", "x_i", size=46)
        self.pilha.poe(A1)
        self.monta(A1, ia1, {}, rt=1.1)

        p_cm = reg.cm
        m_cm = cm_pt(p_cm, 0.095)
        s_mg = seta(p_cm, p_cm + DOWN * 1.45, FC, 6, tip=0.22)
        l_mg = T("Mg", 42, FC).next_to(s_mg, RIGHT, buff=0.16)
        cota_l2 = VGroup(
            Line(P_DOB + 0.42 * UP, p_cm + 0.42 * UP).set_stroke(GEO, 2.6),
            T(r"x_{\mathrm{cm}} = \tfrac{L}{2}", 36, GEO).move_to((P_DOB + p_cm) / 2 + 0.80 * UP),
        )
        self.gat("concentrado no centro de massa")
        self.play(FadeOut(setas_p), FadeIn(m_cm), FadeIn(s_mg), FadeIn(l_mg), FadeIn(cota_l2), run_time=0.9)

        A2, ia2 = M(r"\tau_{\mathrm{peso}}", "=", "M", "g", r"x_{\mathrm{cm}}", size=52)
        self.pilha.poe(A2)
        self.passo(
            A1, A2,
            (J(ia1, 0), J(ia2, 0)),
            (J(ia1, 1), J(ia2, 1)),
            (J(ia1, 7), J(ia2, 3)),
            (J(ia1, 8, 9, 10), J(ia2, 2, 4)),
            rt=1.1,
            origem=True,
        )
        self.foco = A2
        self.ate(0.99)

        # ── T4-2: τ_z = −M g (L/2), I = ⅓ M L² → α_z = −3g / (2L), M riscado, |α| = 14,7 rad/s² ──
        self.an("T4-2")
        self.pilha.limpa()
        B1, ib1 = M(r"\tau_z", "=", "-", "M", "g", r"\frac{L}{2}", size=50)
        self.pilha.poe(B1)
        arco_h = arco_torque(P_DOB, r=0.52, sentido=-1, a0=0.1, amp=1.6, cor=TQ)
        self.play(FadeOut(A0_t4), FadeOut(A1), FadeOut(A2), FadeIn(arco_h), run_time=0.45)
        self.monta(B1, ib1, {3: l_mg, 5: cota_l2[1]}, rt=1.0)
        self.gat("menos massa vezes gravidade")

        B2, ib2 = M("I", "=", r"\frac{1}{3}", "M", "L^2", size=50)
        self.pilha.poe(B2)
        self.gat("um terço da massa")
        self.monta(B2, ib2, {}, rt=0.9)

        B3, ib3 = M(r"\alpha_z", "=", r"\frac{-M g L / 2}{\frac{1}{3} M L^2}", size=48)
        self.pilha.poe(B3)
        self.gat("divide um pelo outro")
        self.monta(B3, ib3, {}, rt=1.0)

        # Risca M em cima e embaixo e L com o quadrado
        self.gat("a massa some")
        risco_M1 = Line(B3[0][3].get_corner(DL), B3[0][3].get_corner(UR)).set_stroke(MAS, 3.8)
        risco_M2 = Line(B3[0][11].get_corner(DL), B3[0][11].get_corner(UR)).set_stroke(MAS, 3.8)
        self.play(Create(risco_M1), Create(risco_M2), run_time=0.6)

        B4, ib4 = M(r"\alpha_z", "=", "-", r"\frac{3g}{2L}", size=56)
        B4b = caixa_l(B4, ACC)
        self.pilha.so(B3, anims=[FadeOut(B1), FadeOut(B2), FadeOut(risco_M1), FadeOut(risco_M2)])
        self.pilha.poe(B4b)
        self.cx(B4b[0])
        self.passo(B3, B4, (J(ib3, 0), J(ib4, 0)), (J(ib3, 1), J(ib4, 1)), rt=1.1, origem=False)
        self.pilha.so(B4b)

        self.selo("CONVENÇÃO DE SINAL", "O SINAL − DIZ: GIRA NO SENTIDO HORÁRIO")

        B5, ib5 = M(r"|\alpha|", "=", r"\frac{3\cdot 9{,}8}{2\cdot 1{,}0}", "=", "14{,}7", r"\,\mathrm{rad/s^2}", size=48)
        self.pilha.poe(B5)
        self.gat("catorze vírgula sete radianos")
        self.monta(B5, ib5, {}, rt=1.1)
        self.foco = B5
        self.ate(0.99)

        # ── T4-3: ω = 0 → a_c = 0; reta a_t(r) = (3g / 2L) r cruzando g em r = 2L/3 ≈ 67 cm; ponta com 3g/2 ──
        self.an("T4-3")
        self.pilha.limpa()
        self.play(FadeOut(VGroup(m_cm, s_mg, l_mg, cota_l2, arco_h, B4b, B5)), run_time=0.45)

        self.selo("INSTANTE DA LARGADA", "PARTINDO DO REPOUSO: SÓ HÁ ACELERAÇÃO TANGENCIAL")

        # Risco explícito em a_c = ω² r = 0 no topo da Pilha
        C0, ic0 = M("a_c", "=", r"\omega^2", "r", "=", "0", size=46)
        self.pilha.poe(C0)
        self.monta(C0, ic0, {}, rt=0.7)
        risco_ac = Line(mp(C0, ic0, [2, 3]).get_corner(DL), mp(C0, ic0, [2, 3]).get_corner(UR)).set_stroke(MAS, 3.6)
        self.play(Create(risco_ac), run_time=0.4)

        # Gráfico sob a régua 2D: linha horizontal tracejada para a aceleração g e reta inclinada para a_t(r) = (3g / 2L) r
        H_G = 1.35
        H_PONTA = 1.5 * H_G
        y_base = P_DOB[1]
        lin_g = DashedLine(P3(P_DOB[0], y_base - H_G), P3(P_DOB[0] + L_ESQ + 0.35, y_base - H_G), dash_length=0.09).set_stroke(GEO, 2.4, opacity=0.85)
        lbl_lin_g = T("g", 38, ACC).next_to(lin_g, RIGHT, buff=0.14)
        reta_at = Line(P_DOB, P3(P_DOB[0] + L_ESQ, y_base - H_PONTA)).set_stroke(ACC, 4.0)

        # Setas verdes de a_t(r) crescendo linearmente com r
        setas_at = VGroup(*[
            seta(P_DOB + RIGHT * (L_ESQ * f), P_DOB + RIGHT * (L_ESQ * f) + DOWN * (H_PONTA * f), ACC, 5, tip=0.17)
            for f in (0.25, 0.50, 2.0 / 3.0, 0.85, 1.00)
        ])

        C1, ic1 = M("a_t(r)", "=", r"|\alpha|", "r", "=", r"\frac{3g}{2L}", "r", size=48)
        self.pilha.poe(C1)
        self.gat("aceleração angular vezes a distância")
        self.play(Create(lin_g), FadeIn(lbl_lin_g), Create(reta_at), FadeIn(setas_at), run_time=1.0)
        self.monta(C1, ic1, {}, rt=1.0)

        # Na ponta (r = L): a_ponta = 3g/2 = 14,7 m/s² > g
        C3, ic3 = M(r"a_{\mathrm{ponta}}", "=", r"\frac{3}{2}", "g", "=", "14{,}7", r"\,\mathrm{m/s^2}", ">", "g", size=48)
        C3b = caixa_l(C3, ACC)
        self.pilha.poe(C3b)
        self.gat("três meios da gravidade")
        self.cx(C3b[0])
        self.monta(C3, ic3, {}, rt=1.1)

        # Ponto crítico r = 2L/3 ≈ 67 cm onde a_t(r) = g
        p_23 = reg.dois_tercos
        dot_23 = Dot(p_23 + DOWN * H_G, radius=0.09, color=WHITE_).set_z_index(18)
        lin_v23 = DashedLine(p_23 + UP * 0.25, p_23 + DOWN * (H_G + 0.25), dash_length=0.07).set_stroke(WHITE_, 2.4)
        lbl_23 = VGroup(T(r"\tfrac{2}{3}L", 36, GEO), nm(r"\approx 67\ \mathrm{cm}", GEO, 36)).arrange(RIGHT, buff=0.10).move_to(dot_23.get_center() + P3(-0.35, -0.48))

        C2, ic2 = M("r", "=", r"\frac{2}{3}", "L", r"\approx", "67", r"\,\mathrm{cm}", r"\ \Rightarrow\ ", "a_t", "=", "g", size=46)
        self.pilha.poe(C2)
        self.gat("dois terços do comprimento")
        self.play(Create(lin_v23), FadeIn(dot_23), FadeIn(lbl_23), run_time=0.8)
        self.monta(C2, ic2, {0: lbl_23[0]}, rt=1.0)

        # Destaca as duas moedas (50 cm < 67 cm e 100 cm > 67 cm)
        m1_2d = RoundedRectangle(width=0.34, height=0.10, corner_radius=0.03).move_to(reg.cm + UP * 0.19).set_fill("#EAF0FA", 0.98).set_stroke(ACC, 2.0)
        m2_2d = RoundedRectangle(width=0.34, height=0.10, corner_radius=0.03).move_to(reg.ponta + UP * 0.36).set_fill("#EAF0FA", 0.98).set_stroke(ACC, 2.0)
        tag_m1 = nm(r"0{,}75\,g < g", ACC, 36).move_to(m1_2d.get_top() + P3(-0.75, 0.30))
        tag_m2 = nm(r"\tfrac{3}{2}g > g", ACC, 36).move_to(m2_2d.get_top() + P3(0.20, 0.30))
        self.gat("a moeda do meio está antes disso")
        self.play(FadeIn(m1_2d), FadeIn(tag_m1), FadeIn(m2_2d), FadeIn(tag_m2), run_time=0.8)
        self.foco = C3b
        self.ate(0.99)

        # ── T4-4: mecanismo físico interno — 12 fatias, forças internas + dobradiça M g / 4 para cima ──
        self.an("T4-4")
        self.sem_selo()
        self.pilha.limpa()
        self.play(
            FadeOut(VGroup(C0, risco_ac, C1, C2, C3b, lin_g, lbl_lin_g, reta_at, setas_at, dot_23, lin_v23, lbl_23, m1_2d, m2_2d, tag_m1, tag_m2)),
            run_time=0.45,
        )

        # Substitui a régua lisa pela régua fatiada em N = 12 fatias
        N_FAT = 12
        reg_fat = regua2d(P_DOB, comp=L_ESQ, esp=0.28, ang=0.0, n_fatias=N_FAT, bancada=True)
        D1, id1 = M(r"F_{\mathrm{alem},i}", "=", "m_i", r"\big(", r"|\alpha|", "r_i", "-", "g", r"\big)", size=46)
        self.pilha.poe(D1)
        self.play(Transform(reg, reg_fat), run_time=0.6)
        self.monta(D1, id1, {}, rt=1.0)

        # Para cada fatia k (k = 0..11), r_k/L = (k + 0.5)/12.
        # A resultante das forças ALÉM DO PESO (para baixo positivo) é F_{alem,k} = m_i (|α| r_k − g) = m_i g (3 r_k / (2L) − 1).
        # Para r_k < 2L/3 (fatias 0..7): F_{alem,k} aponta PARA CIMA (segura a fatia para descer com a < g).
        # Para r_k > 2L/3 (fatias 8..11): F_{alem,k} aponta PARA BAIXO (puxa a fatia para descer com a > g!).
        setas_alem = VGroup()
        vals_alem = []
        for k in range(N_FAT):
            u_k = (k + 0.5) / N_FAT
            f_rel = 1.5 * u_k - 1.0  # negativo = para cima; positivo = para baixo
            vals_alem.append(f_rel)
            pk = P_DOB + RIGHT * (L_ESQ * u_k)
            dy = -1.35 * f_rel       # em Manim: +y é para cima, então f_rel < 0 → dy > 0 (seta para cima)
            y0 = pk[1] + (0.16 if dy > 0 else -0.16)
            setas_alem.add(seta(P3(pk[0], y0), P3(pk[0], y0 + dy), FC, 4.8, tip=0.16))

        tit_setas = txt("FORÇAS ALÉM DO PESO (VIZINHOS + DOBRADIÇA)", 22, bold=True, color=FC).move_to(P_DOB + P3(2.4, -1.55))
        self.gat("olha cada fatia")
        self.play(FadeIn(setas_alem), FadeIn(tit_setas), run_time=0.9)

        # Registra para auditoria FATIAS em qa22.py
        self.reg("fatias_t4", n=N_FAT, f_rel=vals_alem, soma_f_rel=sum(vals_alem))

        # Na fatia 0 (colada à dobradiça), separa a seta em VIZINHOS (internos) + DOBRADIÇA (externa = M g / 4 para cima)
        s_dob = seta(P_DOB + P3(0.0, 0.20), P_DOB + P3(0.0, 1.35), FC, 6.5, tip=0.20)
        l_dob_f = VGroup(txt("DOBRADIÇA:", 22, bold=True, color=FC), T(r"\tfrac{1}{4}Mg", 36, FC)).arrange(RIGHT, buff=0.10).move_to(P_DOB + P3(0.95, 1.68))

        self.gat("perto da dobradiça")

        D2, id2 = M(r"r_i > \tfrac{2}{3}L", r"\ \Rightarrow\ ", r"F_{\mathrm{viz}} < 0", size=46)
        self.pilha.poe(D2)
        self.gat("depois dos dois terços")
        self.monta(D2, id2, {}, rt=0.7)

        # Soma de todas as fatias: pares internos cancelam, sobra a reação da dobradiça F_dob = M g / 4 para cima
        D3a, id3a = M(r"F_{\mathrm{dob}}", "=", "M", "g", "-", "M", r"a_{\mathrm{cm}}", size=46)
        D3b, id3b = M(r"F_{\mathrm{dob}}", "=", "M", "g", "-", "M", r"\frac{3g}{4}", "=", r"\frac{1}{4}", "M", "g", size=46)
        self.pilha.poe(D3a)
        self.pilha.poe(D3b)
        self.gat("um quarto do peso")
        self.play(FadeIn(s_dob), FadeIn(l_dob_f), run_time=0.7)
        self.monta(D3a, id3a, {}, rt=0.6)
        self.monta(D3b, id3b, {}, rt=0.8)

        self.selo("FÍSICA INTERNA", "NÃO HÁ NADA VIOLANDO A GRAVIDADE: A RÉGUA INTEIRA PUXA A PONTA")
        self.foco = D3b
        self.ate(0.99)

        # ── T4-5: vassoura (1,2 m) vs lápis (15 cm) tombando da vertical com RK4 de θ̈ = (3g / 2L) sen θ ──
        self.an("T4-5")
        self.sem_selo()
        self.pilha.limpa()
        self.play(
            FadeOut(VGroup(reg, setas_alem, tit_setas, s_dob, l_dob_f, D1, D2, D3a, D3b)),
            run_time=0.45,
        )

        # Chão na esquerda + vassoura e lápis apoiados lado a lado
        P_VAS = P3(-5.8, -2.55)
        P_LAP = P3(-2.3, -2.55)
        chao_vl = Line(P3(-6.8, -2.55), P3(-0.6, -2.55)).set_stroke(GEO, 2.8)
        t_vl = ValueTracker(0.0)
        self.add(t_vl)

        dt_vl = TAB_VASSOURA["dt"]
        tv_max = float(TAB_VASSOURA["t_queda"])
        tl_max = float(TAB_LAPIS["t_queda"])

        def _cena_vl():
            tf = t_vl.get_value()
            idx = min(len(TAB_VASSOURA["ts"]) - 1, max(0, int(round(tf / dt_vl))))
            th_v = float(TAB_VASSOURA["th"][idx])
            th_l = float(TAB_LAPIS["th"][idx])
            v_obj = vassoura(P_VAS, comp=3.6, th=th_v)
            l_obj = lapis(P_LAP, comp=0.75, th=th_l)
            tv_mostra = min(tf, tv_max)
            tl_mostra = min(tf, tl_max)
            rel_v = VGroup(txt("VASSOURA (1,2 m)", 22, color=GEO), nm(rf"t = {br(tv_mostra, 2)}\ \mathrm{{s}}", VEL, 36)).arrange(DOWN, buff=0.08).move_to(P3(-5.5, 2.05))
            rel_l = VGroup(txt("LÁPIS (15 cm)", 22, color=GEO), nm(rf"t = {br(tl_mostra, 2)}\ \mathrm{{s}}", VEL, 36)).arrange(DOWN, buff=0.08).move_to(P3(-2.1, 2.05))
            return VGroup(chao_vl, v_obj, l_obj, rel_v, rel_l)

        v_vl = vivo(_cena_vl)
        E1, ie1 = M(r"|\alpha|", "=", r"\frac{3g}{2L}", r"\sin\theta", r"\ \propto\ ", r"\frac{1}{L}", size=48)
        self.pilha.poe(E1)
        self.play(FadeIn(v_vl), run_time=0.6)
        self.monta(E1, ie1, {}, rt=1.0)
        self.gat("um sobre o comprimento")

        # Anima a queda RK4 até a vassoura bater no chão
        self.gat("oito vezes mais curto")
        self.play(t_vl.animate.set_value(tv_max + 0.02), run_time=2.6, rate_func=linear)

        E2, ie2 = M(r"\frac{L_{\mathrm{vassoura}}}{L_{\mathrm{lapis}}}", "=", r"\frac{1{,}20}{0{,}15}", "=", "8", size=48)
        self.pilha.poe(E2)
        self.monta(E2, ie2, {}, rt=0.9)

        E3, ie3 = M(r"\frac{t_{\mathrm{vassoura}}}{t_{\mathrm{lapis}}}", "=", r"\sqrt{8}", r"\approx", "2{,}8", size=52)
        E3b = caixa_l(E3, ACC)
        self.pilha.poe(E3b)
        self.gat("duas vírgula oito vezes menor")
        self.cx(E3b[0])
        self.monta(E3, ie3, {}, rt=1.0)
        self.foco = E3b
        self.ate(0.99)
