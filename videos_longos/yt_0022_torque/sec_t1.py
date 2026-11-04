"""Lote PT1: T1 — O QUE É TORQUE E O BRAÇO DE ALAVANCA.
T1-1 e T1-2: Three.js 'porta' vista de cima. F = 20 N a r = 0,15 m vs r = 0,75 m (maçaneta), e depois na maçaneta em φ = 90°, 30°, 0°
(com LINHA DE AÇÃO tracejada passando pela dobradiça).
T1-3: esquema 2D da porta vista de cima com as duas leituras equivalentes lado a lado: r_⊥ = r sen φ (BRAÇO DE ALAVANCA) e F_⊥ = F sen φ,
convergindo para τ = r F sen φ = r_⊥ F = r F_⊥ em caixa PANEL azul-força.
T1-4: convenção de sinal (+ anti-horário, − horário), unidade [τ] = N·m e J riscado (N·m ≠ J: torque não é energia).
T1-5: chave de roda 2,5D (r = 0,40 m, F = 250 N → τ = 100 N·m; a 30° → 50 N·m; com cano de 0,80 m e 125 N → 100 N·m)."""
from pecas22 import *  # noqa: F401,F403


class LoteT1(Lote22):
    def corpo(self):
        cam = cam_porta_topo()
        ang_p = ValueTracker(0.0)
        self.add(ang_p)

        def est(t):
            a = ang_p.get_value()
            e = {"ang": a, "cam": cam, "piso": False, "z_ref": 0.0}
            if not PEDIDOS3D:
                self.reg(
                    "t1_porta",
                    ang=a,
                    dob_meio=tela_porta(cam, 0.0, a, 0.0),
                    perto=tela_porta(cam, 0.15, a, 0.0),
                    macaneta=tela_porta(cam, 0.75, a, 0.0),
                )
            return r4(e)

        f3 = Fundo3D(self, "porta", est)
        self.add(f3)
        self.f3 = f3
        self.secao("TORQUE E BRAÇO DE ALAVANCA")

        # ── T1-1: mesma força F = 20 N a r = 0,15 m vs r = 0,75 m (maçaneta) ──
        self.an("T1-1")
        p_dob = P3(*tela_porta(cam, 0.0, 0.0), 0.0)
        p_perto = P3(*tela_porta(cam, 0.15, 0.0), 0.0)
        p_mac = P3(*tela_porta(cam, 0.75, 0.0), 0.0)

        lbl_dob = txt("DOBRADIÇA", 24, color=GEO).move_to(p_dob + P3(0.0, -0.68))
        lbl_mac = txt("MAÇANETA", 24, color=GEO).move_to(p_mac + P3(0.0, -0.68))
        cab_t1 = txt("MESMA FORÇA, DISTÂNCIAS DIFERENTES:", 26, bold=True, color=TQ)
        self.pilha.poe(cab_t1)
        self.play(FadeIn(lbl_dob), FadeIn(lbl_mac), FadeIn(cab_t1), run_time=0.7)

        # F = 20 N em r = 0,15 m
        s_f1 = seta(p_perto + P3(0.0, -1.45), p_perto + P3(0.0, -0.10), FC, 6, tip=0.22)
        l_f1 = VGroup(T("F=", 38, FC), nm(r"20\ \mathrm{N}", FC, 38)).arrange(RIGHT, buff=0.08).next_to(s_f1, DOWN, buff=0.18)
        c_r1 = VGroup(
            Line(p_dob + 0.42 * UP, p_perto + 0.42 * UP).set_stroke(GEO, 2.8),
            nm(r"0{,}15\ \mathrm{m}", GEO, 36).move_to((p_dob + p_perto) / 2 + 0.78 * UP),
        )
        self.gat("vinte newtons")
        self.play(FadeIn(s_f1), FadeIn(l_f1), run_time=0.7)

        self.gat("perto da dobradiça")
        self.play(FadeIn(c_r1), ang_p.animate.set_value(0.06), run_time=1.1)

        # Na direita (coluna da Pilha), registra a comparação direta
        card1 = VGroup(
            txt("PERTO DO EIXO:", 26, color=GEO),
            VGroup(T("r=", 42, GEO), nm(r"0{,}15\ \mathrm{m}", GEO, 42), T(r"\ \Rightarrow\ ", 42), txt("QUASE NÃO GIRA", 26, bold=True)).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        self.pilha.poe(card1)
        self.play(FadeIn(card1, shift=0.1 * UP), run_time=0.7)

        self.gat("lá na maçaneta")
        self.play(ang_p.animate.set_value(0.0), FadeOut(s_f1), FadeOut(c_r1), run_time=0.5)
        s_f2 = seta(p_mac + P3(0.0, -1.45), p_mac + P3(0.0, -0.10), FC, 6, tip=0.22)
        c_r2 = VGroup(
            Line(p_dob + 0.42 * UP, p_mac + 0.42 * UP).set_stroke(GEO, 2.8),
            nm(r"0{,}75\ \mathrm{m}", GEO, 36).move_to((p_dob + p_mac) / 2 + 0.78 * UP),
        )
        self.play(FadeIn(s_f2), l_f1.animate.next_to(s_f2, DOWN, buff=0.18), FadeIn(c_r2), ang_p.animate.set_value(0.42), run_time=1.3)

        card2 = VGroup(
            txt("NA MAÇANETA:", 26, color=GEO),
            VGroup(T("r=", 42, GEO), nm(r"0{,}75\ \mathrm{m}", GEO, 42), T(r"\ \Rightarrow\ ", 42), txt("ABRE FÁCIL", 26, bold=True, color=TQ)).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        self.pilha.poe(card2)
        self.play(FadeIn(card2, shift=0.1 * UP), run_time=0.7)
        self.foco = card2
        self.ate(0.99)

        # ── T1-2: na mesma maçaneta, φ = 90°, 30° e 0° (LINHA DE AÇÃO passa pelo eixo) ──
        self.an("T1-2")
        self.pilha.limpa()
        cab_t12 = txt("O QUE DECIDE O GIRO:", 28, bold=True, color=TQ)
        self.pilha.poe(cab_t12)
        self.play(FadeOut(cab_t1), FadeOut(card1), FadeOut(card2), FadeOut(lbl_mac), FadeOut(lbl_dob), FadeIn(cab_t12), ang_p.animate.set_value(0.0), run_time=0.5)

        # φ = 90°
        arco_90 = RightAngle(Line(p_mac, p_dob), Line(p_mac, p_mac + UP), length=0.26, color=GEO)
        lbl_90 = nm(r"90^\circ", GEO, 36).move_to(p_mac + P3(-0.48, -0.48))
        self.gat("perpendicular à porta")
        self.play(FadeIn(arco_90), FadeIn(lbl_90), ang_p.animate.set_value(0.36), run_time=1.1)
        self.play(ang_p.animate.set_value(0.0), run_time=0.5)

        # φ = 30°
        self.gat("inclinando a força")
        ang_30 = math.radians(30.0)
        dir_30 = np.array([-math.cos(ang_30), math.sin(ang_30), 0.0])
        s_f30 = seta(p_mac - dir_30 * 1.45, p_mac - dir_30 * 0.10, FC, 6, tip=0.22)
        lbl_30 = nm(r"30^\circ", GEO, 36).move_to(p_mac + P3(-0.68, -0.42))
        self.play(FadeOut(arco_90), Transform(s_f2, s_f30), Transform(lbl_90, lbl_30), l_f1.animate.next_to(s_f30, DOWN, buff=0.18), ang_p.animate.set_value(0.16), run_time=1.1)
        self.play(ang_p.animate.set_value(0.0), run_time=0.4)

        # φ = 0° (apontando para a dobradiça) + LINHA DE AÇÃO tracejada
        self.gat("apontando para a dobradiça")
        s_f0 = seta(p_mac + P3(1.45, 0.0), p_mac + P3(0.10, 0.0), FC, 6, tip=0.22)
        lin_acao = DashedLine(p_dob + P3(-0.75, 0.0), p_mac + P3(1.55, 0.0), dash_length=0.10).set_stroke(GEO, 2.4, opacity=0.85)
        lbl_la = txt("LINHA DE AÇÃO PASSA PELO EIXO", 24, color=GEO).move_to((p_dob + p_mac) / 2 + P3(0.2, -0.72))
        self.play(Transform(s_f2, s_f0), FadeOut(lbl_90), l_f1.animate.next_to(s_f0, UP, buff=0.22), Create(lin_acao), FadeIn(lbl_la), run_time=0.9)

        # Resumo dos 3 ingredientes na Pilha
        self.gat("importam três coisas")
        ing = VGroup(
            VGroup(T(r"1.\ ", 38, GEO), T("F", 46, FC), txt("TAMANHO DA FORÇA", 26)).arrange(RIGHT, buff=0.18),
            VGroup(T(r"2.\ ", 38, GEO), T("r", 46, GEO), txt("DISTÂNCIA AO EIXO", 26)).arrange(RIGHT, buff=0.18),
            VGroup(T(r"3.\ ", 46, GEO), T(r"\varphi", 46, GEO), txt("ÂNGULO ENTRE ELAS", 26)).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        self.pilha.poe(ing)
        self.play(FadeIn(ing, shift=0.12 * UP), run_time=0.9)
        self.foco = ing
        self.ate(0.99)

        # ── T1-3: esquema 2D limpo + as duas leituras (r_⊥ = r sen φ e F_⊥ = F sen φ) → caixa PANEL τ ──
        self.an("T1-3")
        self.pilha.limpa()
        self.play(
            f3.op.animate.set_value(0.0),
            FadeOut(VGroup(cab_t12, s_f2, l_f1, c_r2, lin_acao, lbl_la, ing)),
            run_time=0.5,
        )

        # Dois esquemas 2D empilhados na esquerda: em cima (1º jeito: braço de alavanca r_⊥), embaixo (2º jeito: força perpendicular F_⊥)
        O1 = P3(-5.8, 1.05)
        L_ESQ = 3.2
        phi = math.radians(38.0)
        P_ap1 = O1 + RIGHT * L_ESQ
        u_f = np.array([math.cos(phi), math.sin(phi), 0.0])
        porta_sup = porta2d(O1, comp=L_ESQ, esp=0.18, ang=0.0)
        s_F_sup = seta(P_ap1, P_ap1 + u_f * 1.35, FC, 6, tip=0.20)
        l_F_sup = T("F", 38, FC).next_to(P_ap1 + u_f * 1.35, RIGHT, buff=0.14)
        l_r_sup = T("r", 38, GEO).move_to(O1 + RIGHT * (L_ESQ * 0.52) + DOWN * 0.38)
        arco_phi1 = Arc(radius=0.52, start_angle=0.0, angle=phi, arc_center=P_ap1).set_stroke(GEO, 2.4)
        l_phi1 = T(r"\varphi", 36, GEO).move_to(P_ap1 + P3(0.76, 0.24))

        A, ia = M(r"\tau", "=", "r", "F", r"\sin\varphi", size=54)
        self.pilha.poe(A)
        self.play(FadeIn(porta_sup), FadeIn(s_F_sup), FadeIn(l_F_sup), FadeIn(l_r_sup), Create(arco_phi1), FadeIn(l_phi1), run_time=0.7)
        self.monta(A, ia, {2: l_r_sup, 3: l_F_sup, 4: l_phi1}, rt=1.1)
        self.gat("o torque é a distância ao eixo vezes a força vezes o seno")

        # 1º jeito: linha de ação tracejada + perpendicular r_⊥ do eixo até a linha de ação
        self.gat("primeiro jeito")
        p_pe_perp = O1 + (L_ESQ * math.sin(phi)) * np.array([math.sin(phi), -math.cos(phi), 0.0])
        lin_ac1 = DashedLine(P_ap1 - u_f * 2.75, P_ap1 + u_f * 1.55, dash_length=0.09).set_stroke(GEO, 2.0, opacity=0.75)
        seg_rperp = Line(O1, p_pe_perp).set_stroke(GEO, 5.0)
        ang_reto1 = RightAngle(Line(p_pe_perp, O1), Line(p_pe_perp, P_ap1), length=0.20, color=GEO)
        l_rperp = T(r"r_\perp = r\sin\varphi", 36, GEO).move_to(O1 + P3(-0.65, -0.88))
        tag_braco = txt("BRAÇO DE ALAVANCA", 22, bold=True, color=GEO).next_to(l_rperp, DOWN, buff=0.08)
        self.play(Create(lin_ac1), Create(seg_rperp), FadeIn(ang_reto1), FadeIn(l_rperp), FadeIn(tag_braco), run_time=0.9)

        B, ib = M(r"\tau", "=", r"r_\perp", "F", size=52)
        self.pilha.poe(B)
        self.gat("torque é força vezes braço de alavanca")
        self.passo(A, B, (J(ia, 0), J(ib, 0)), (J(ia, 1), J(ib, 1)), (J(ia, 2, 4), J(ib, 2)), (J(ia, 3), J(ib, 3)), rt=1.1, origem=True)

        # 2º jeito: esquema inferior separando F em F_∥ (ao longo de r) e F_⊥ (perpendicular a r)
        self.gat("segundo jeito")
        O2 = P3(-5.8, -1.95)
        P_ap2 = O2 + RIGHT * L_ESQ
        porta_inf = porta2d(O2, comp=L_ESQ, esp=0.18, ang=0.0)
        s_F_inf = seta(P_ap2, P_ap2 + u_f * 1.45, FC, 4, tip=0.18, op=0.45)
        s_Fpar = seta(P_ap2, P_ap2 + RIGHT * (1.45 * math.cos(phi)), GEO, 4, tip=0.16, op=0.65)
        l_Fpar = T(r"F_\parallel", 32, GEO).next_to(s_Fpar, DOWN, buff=0.10)
        s_Fperp = seta(P_ap2, P_ap2 + UP * (1.45 * math.sin(phi)), FC, 6, tip=0.20)
        l_Fperp = T(r"F_\perp = F\sin\varphi", 34, FC).next_to(s_Fperp, LEFT, buff=0.14)
        self.play(FadeIn(porta_inf), FadeIn(s_F_inf), FadeIn(s_Fpar), FadeIn(l_Fpar), FadeIn(s_Fperp), FadeIn(l_Fperp), run_time=0.9)

        C_, ic = M(r"\tau", "=", "r", r"F_\perp", size=52)
        self.pilha.poe(C_)
        self.gat("quem gira é a parte perpendicular")
        self.passo(A, C_, (J(ia, 0), J(ic, 0)), (J(ia, 1), J(ic, 1)), (J(ia, 2), J(ic, 2)), (J(ia, 3, 4), J(ic, 3)), rt=1.1, origem=True)

        # Caixa PANEL azul-força unindo as três leituras
        self.gat("é a mesma conta lida pelos dois lados")
        D_, id_ = M(r"\tau", "=", "r", "F", r"\sin\varphi", "=", r"r_\perp", "F", "=", "r", r"F_\perp", size=48)
        Db = caixa_l(D_, TQ)
        self.pilha.so(A, B, C_)
        self.pilha.poe(Db)
        self.cx(Db[0])
        self.voa(
            [
                (mp(A, ia, [0, 1, 2, 3, 4]), mp(D_, id_, [0, 1, 2, 3, 4])),
                (mp(B, ib, [2, 3]), mp(D_, id_, [6, 7])),
                (mp(C_, ic, [2, 3]), mp(D_, id_, [9, 10])),
            ],
            extra=[],
            rt=1.1,
            origem=False,
            escrever=[mp(D_, id_, [5]), mp(D_, id_, [8])],
        )
        self.pilha.so(Db)
        self.foco = Db
        self.ate(0.99)

        # ── T1-4: convenção de sinal (+ anti-horário, − horário) e unidade [τ] = N·m ≠ J ──
        self.an("T1-4")
        self.play(
            FadeOut(VGroup(porta_sup, s_F_sup, l_F_sup, l_r_sup, arco_phi1, l_phi1, lin_ac1, seg_rperp, ang_reto1, l_rperp, tag_braco)),
            FadeOut(VGroup(porta_inf, s_F_inf, s_Fpar, l_Fpar, s_Fperp, l_Fperp)),
            run_time=0.45,
        )

        # Dois mostradores circulares na esquerda: + ANTI-HORÁRIO e − HORÁRIO
        c_pos, c_neg = P3(-4.8, 0.85), P3(-2.0, 0.85)
        d_pos = VGroup(
             disco_aco(c_pos, 0.95),
            eixo_cruz(c_pos, 0.14),
            arco_torque(c_pos, r=0.65, sentido=1, a0=-0.2, amp=2.2, cor=TQ),
            T(r"\tau > 0\ (+)", 38, TQ).move_to(c_pos + P3(0.0, -1.35)),
            txt("ANTI-HORÁRIO", 22, color=GEO).move_to(c_pos + P3(0.0, -1.78)),
        )
        d_neg = VGroup(
            disco_aco(c_neg, 0.95),
            eixo_cruz(c_neg, 0.14),
            arco_torque(c_neg, r=0.65, sentido=-1, a0=2.0, amp=2.2, cor=TQ),
            T(r"\tau < 0\ (-)", 38, TQ).move_to(c_neg + P3(0.0, -1.35)),
            txt("HORÁRIO", 22, color=GEO).move_to(c_neg + P3(0.0, -1.78)),
        )
        self.gat("girar no anti horário é positivo")
        self.play(FadeIn(d_pos, shift=0.1 * UP), run_time=0.7)
        self.gat("e no horário é negativo")
        self.play(FadeIn(d_neg, shift=0.1 * UP), run_time=0.7)

        # Unidade N·m e distinção em relação ao Joule (J riscado)
        U1, iu1 = M(r"[\tau]", "=", r"\mathrm{N\cdot m}", size=52)
        self.pilha.poe(U1)
        self.gat("a unidade é newton vezes metro")
        self.monta(U1, iu1, {}, rt=0.8)

        U2, iu2 = M(r"\mathrm{N\cdot m}", r"\neq", r"\mathrm{J}", size=52)
        l_u2 = VGroup(U2, txt("(TORQUE ≠ ENERGIA)", 26, bold=True, color=KC)).arrange(RIGHT, buff=0.24)
        self.pilha.poe(l_u2)
        self.gat("mas torque não é energia")
        self.monta(U2, iu2, {0: mp(U1, iu1, [2])}, rt=0.9)
        self.play(FadeIn(l_u2[1]), run_time=0.4)
        risco_J = Line(mp(U2, iu2, [2]).get_corner(DL) + 0.06 * DL, mp(U2, iu2, [2]).get_corner(UR) + 0.06 * UR).set_stroke(MAS, 4.0)
        self.gat("ninguém escreve joule no torque")
        self.play(Create(risco_J), run_time=0.5)
        self.foco = l_u2
        self.ate(0.99)

        # ── T1-5: exemplo da chave de roda (0,40 m × 250 N = 100 N·m; a 30° → 50 N·m; com cano de 0,80 m e 125 N → 100 N·m) ──
        self.an("T1-5")
        self.pilha.limpa()
        cab_t15 = txt("EXEMPLO: CHAVE DE RODA", 26, bold=True, color=TQ)
        self.pilha.poe(cab_t15)
        self.play(FadeOut(VGroup(d_pos, d_neg, Db, U1, l_u2, risco_J)), FadeIn(cab_t15), run_time=0.45)

        P_porca = P3(-5.8, -0.35)
        L_CH = 2.6
        chave = chave_roda(P_porca, comp=L_CH, ang=0.0, cano=False)
        cota_04 = VGroup(
            Line(P_porca + 0.55 * UP, chave.ponta + 0.55 * UP).set_stroke(GEO, 2.6),
            nm(r"0{,}40\ \mathrm{m}", GEO, 36).move_to((P_porca + chave.ponta) / 2 + 0.90 * UP),
        )
        s_250 = seta(chave.ponta + P3(0.0, -1.55), chave.ponta + P3(0.0, -0.14), FC, 6, tip=0.22)
        l_250 = nm(r"250\ \mathrm{N}", FC, 38).next_to(s_250, DOWN, buff=0.16)
        arco_t = arco_torque(P_porca, r=0.52, sentido=1, a0=0.4, amp=1.9, cor=TQ)

        self.play(FadeIn(chave), FadeIn(cota_04), FadeIn(s_250), FadeIn(l_250), FadeIn(arco_t), run_time=0.8)

        E1, ie1 = M(r"\tau", "=", "0{,}40", r"\cdot", "250", "=", "100", r"\,\mathrm{N\cdot m}", size=50)
        self.pilha.poe(E1)
        self.gat("cem newtons metro")
        self.monta(E1, ie1, {2: cota_04[1], 4: l_250}, rt=1.1)

        # Inclinado a 30° → τ = 50 N·m
        self.gat("a trinta graus da chave")
        u30 = np.array([-math.cos(math.radians(30)), math.sin(math.radians(30)), 0.0])
        s_250_30 = seta(chave.ponta - u30 * 1.55, chave.ponta - u30 * 0.14, FC, 6, tip=0.22)
        l_ang30 = nm(r"30^\circ", GEO, 36).move_to(chave.ponta + P3(-0.65, -0.45))
        self.play(Transform(s_250, s_250_30), l_250.animate.next_to(s_250_30, DOWN, buff=0.16), FadeIn(l_ang30), run_time=0.7)

        E2, ie2 = M(r"\tau_{30^\circ}", "=", "100", r"\cdot", "0{,}5", "=", "50", r"\,\mathrm{N\cdot m}", size=48)
        self.pilha.poe(E2)
        self.gat("cai para cinquenta")
        self.monta(E2, ie2, {4: l_ang30}, rt=1.0)

        # Cano extensor de 0,80 m com metade da força (125 N) → mesmos 100 N·m
        self.gat("encaixa um cano na chave")
        chave_c = chave_roda(P_porca, comp=L_CH, ang=0.0, cano=True, comp_cano=4.8)
        cota_08 = VGroup(
            Line(P_porca + 0.55 * UP, chave_c.ponta + 0.55 * UP).set_stroke(GEO, 2.6),
            nm(r"0{,}80\ \mathrm{m}", GEO, 36).move_to((P_porca + chave_c.ponta) / 2 + 0.90 * UP),
        )
        s_125 = seta(chave_c.ponta + P3(0.0, -0.95), chave_c.ponta + P3(0.0, -0.14), FC, 6, tip=0.20)
        l_125 = nm(r"125\ \mathrm{N}", FC, 38).next_to(s_125, DOWN, buff=0.12)
        self.play(
            FadeOut(l_ang30),
            Transform(chave, chave_c),
            Transform(cota_04, cota_08),
            Transform(s_250, s_125),
            Transform(l_250, l_125),
            run_time=0.9,
        )

        E3, ie3 = M(r"\tau", "=", "0{,}80", r"\cdot", "125", "=", "100", r"\,\mathrm{N\cdot m}", size=50)
        self.pilha.poe(E3)
        self.gat("os mesmos cem newtons metro")
        self.monta(E3, ie3, {2: cota_04[1], 4: l_250}, rt=1.0)
        self.foco = E3
        self.ate(0.99)
