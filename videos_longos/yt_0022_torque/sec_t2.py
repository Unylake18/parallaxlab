"""Lote PT2: T2 — TORQUE COMO VETOR: O PRODUTO VETORIAL.
T2-1 e T2-2: Three.js 'porta' que orbita da vista de cima até a vista 3/4 e PARA. Em Manim (projeta3d): vetor posição r⃗ em âmbar (#D2823A),
força F⃗ em azul-força (#5AA2FF), paralelogramo semitransparente (ÁREA = r F sen φ), vetor τ⃗ = r⃗ × F⃗ subindo pelo eixo da dobradiça com arco
de sentido e ícone 2D da regra da mão direita.
T2-3: esquema 2D onde o paralelogramo afina quando φ → 0° (F⃗ ∥ r⃗ ⇒ τ⃗ = 0⃗) e troca a ordem r⃗ × F⃗ = −F⃗ × r⃗.
T2-4: componentes x, y e fórmula τ_z = x F_y − y F_x testada na chave de roda (0,40 · 250 − 0 · 0 = 100 N·m).
T2-5: chave de roda com dois pontos O (porca, 0,40 m) e P (meio do cabo, 0,20 m): τ_O = 100 N·m vs τ_P = 50 N·m e selo 'SEMPRE DIGA: TORQUE EM RELAÇÃO A QUAL PONTO'."""
from pecas22 import *  # noqa: F401,F403


class LoteT2(Lote22):
    def corpo(self):
        u_cam = ValueTracker(0.0)
        ang_p = ValueTracker(0.18)
        self.add(u_cam, ang_p)

        def est(t):
            u = float(u_cam.get_value())
            a = float(ang_p.get_value())
            cam = cam_porta_obl(u)
            e = {"ang": a, "cam": cam, "piso": bool(u > 0.15), "z_ref": 0.0}
            if not PEDIDOS3D:
                self.reg(
                    "t2_porta",
                    u_cam=u,
                    ang=a,
                    dob_meio=tela_porta(cam, 0.0, a, 0.0),
                    dob_base=projeta3d(cam, (0.0, 0.0, -0.80)),
                    dob_topo=projeta3d(cam, (0.0, 0.0, 0.80)),
                    macaneta=tela_porta(cam, 0.75, a, 0.0),
                )
            return r4(e)

        f3 = Fundo3D(self, "porta", est)
        self.add(f3)
        self.f3 = f3
        self.secao("TORQUE COMO VETOR")

        # ── T2-1: câmera orbita do topo até 3/4 e PARA; entram r⃗, F⃗ e o paralelogramo de área r F sen φ ──
        self.an("T2-1")
        cab_t2 = txt("VETORES NO ESPAÇO 3D:", 26, bold=True, color=TQ)
        self.pilha.poe(cab_t2)
        self.play(FadeIn(cab_t2), u_cam.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        cam_34 = cam_porta_obl(1.0)
        a0 = ang_p.get_value()

        p_dob = P3(*tela_porta(cam_34, 0.0, a0, 0.0), 0.0)
        p_mac = P3(*tela_porta(cam_34, 0.75, a0, 0.0), 0.0)
        p_topo = P3(*projeta3d(cam_34, (0.0, 0.0, 0.65)), 0.0)
        # Ponto final de F⃗ no plano z = 0 (perpendicular à porta no sentido anti-horário)
        u_f3d = (-math.sin(a0) * 0.45, math.cos(a0) * 0.45, 0.0)
        p_fim_f = P3(*projeta3d(cam_34, (0.75 * math.cos(a0) + u_f3d[0], 0.75 * math.sin(a0) + u_f3d[1], 0.0)), 0.0)

        s_r = seta(p_dob, p_mac, VETC, 6, tip=0.22)
        l_r = T(r"\vec r", 42, VETC).move_to((p_dob + p_mac) / 2 + P3(0.0, -0.40))
        s_F = seta(p_mac, p_fim_f, FC, 6, tip=0.22)
        l_F = T(r"\vec F", 42, FC).next_to(p_fim_f, RIGHT, buff=0.18)

        self.gat("olha a porta de um ângulo diferente")
        self.play(FadeIn(s_r), FadeIn(l_r), FadeIn(s_F), FadeIn(l_F), run_time=0.8)

        # Quarto vértice do paralelogramo projetado em perspectiva exata
        p_quarto = P3(*projeta3d(cam_34, (u_f3d[0], u_f3d[1], 0.0)), 0.0)
        paral = Polygon(p_dob, p_mac, p_fim_f, p_quarto).set_fill(TQ, 0.26).set_stroke(TQ, 2.2)
        lbl_area = VGroup(txt("ÁREA =", 24, bold=True, color=TQ), T(r"r F\sin\varphi", 36)).arrange(RIGHT, buff=0.12).move_to(
            (p_dob + p_mac + p_fim_f + p_quarto) / 4 + P3(-0.35, 0.42)
        )
        self.gat("desenha o paralelogramo")
        self.play(FadeIn(paral), FadeIn(lbl_area), run_time=0.9)

        B, ib = M(r"|\vec\tau|", "=", "r", "F", r"\sin\varphi", size=50)
        l_b = VGroup(B, txt("= ÁREA", 26, bold=True, color=TQ)).arrange(RIGHT, buff=0.22)
        self.pilha.poe(l_b)
        self.gat("exatamente o tamanho do torque")
        self.monta(B, ib, {}, rt=0.9)
        self.play(FadeIn(l_b[1]), run_time=0.4)
        self.foco = l_b
        self.ate(0.99)

        # ── T2-2: direção ao longo do eixo + regra da mão direita + τ⃗ = r⃗ × F⃗ em caixa PANEL azul-força ──
        self.an("T2-2")
        s_tau = seta(p_dob, p_topo, TQ, 7, tip=0.24)
        l_tau = T(r"\vec\tau", 46, TQ).next_to(p_topo, LEFT, buff=0.16)
        arco_eixo = arco_torque(p_dob + P3(0.0, 0.55), r=0.38, sentido=1, a0=-0.4, amp=2.2, cor=TQ, w=4.5, tip=0.16)
        self.gat("ao longo do eixo de giro")
        self.play(FadeIn(s_tau), FadeIn(l_tau), FadeIn(arco_eixo), run_time=0.9)

        ic_mao = mao_direita(P3(-1.45, 1.15), escala=0.88, sentido=1)
        self.gat("regra da mão direita")
        self.play(FadeIn(ic_mao, shift=0.1 * UP), run_time=0.7)

        A, ia = M(r"\vec\tau", "=", r"\vec r", r"\times", r"\vec F", size=58)
        Ab = caixa_l(A, TQ)
        self.pilha.poe(Ab)
        self.gat("produto vetorial")
        self.cx(Ab[0])
        self.monta(A, ia, {0: l_tau, 2: l_r, 4: l_F}, rt=1.1)
        self.foco = Ab
        self.ate(0.99)

        # ── T2-3: F⃗ ∥ r⃗ ⇒ τ⃗ = 0⃗ (paralelogramo afina até linha) e troca da ordem r⃗ × F⃗ = −F⃗ × r⃗ ──
        self.an("T2-3")
        self.play(
            f3.op.animate.set_value(0.0),
            FadeOut(VGroup(s_r, l_r, s_F, l_F, s_tau, l_tau, arco_eixo, paral, lbl_area, ic_mao)),
            run_time=0.45,
        )

        # Esquema 2D limpo na esquerda mostrando o paralelogramo entre r⃗ e F⃗
        O_p = P3(-5.5, 0.55)
        phi_tr = ValueTracker(math.radians(55.0))
        inv_tr = ValueTracker(1.0)
        self.add(phi_tr, inv_tr)

        def _des_paral():
            ph = phi_tr.get_value()
            sinal = inv_tr.get_value()
            vr = P3(2.8, 0.0)
            vf = P3(1.8 * math.cos(ph), 1.8 * math.sin(ph) * sinal)
            pol = Polygon(O_p, O_p + vr, O_p + vr + vf, O_p + vf).set_fill(TQ, 0.25 * abs(math.sin(ph))).set_stroke(TQ, 2.0)
            sr = seta(O_p, O_p + vr, VETC, 6, tip=0.20)
            lr = T(r"\vec r", 40, VETC).next_to(sr, DOWN if sinal >= 0 else UP, buff=0.12)
            sf = seta(O_p, O_p + vf, FC, 6, tip=0.20)
            lf = T(r"\vec F", 40, FC).next_to(O_p + vf, UL if sinal >= 0 else DL, buff=0.10)
            # Símbolo de τ⃗ apontando para fora (⊙) ou para dentro (⊗)
            c_simb = O_p + P3(1.4, -1.65)
            circ_s = Circle(radius=0.24).move_to(c_simb).set_stroke(TQ, 2.8)
            if abs(math.sin(ph)) < 0.05:
                miolo = T("0", 34, GEO).move_to(c_simb)
            elif sinal >= 0:
                miolo = Dot(c_simb, radius=0.065, color=TQ)
            else:
                miolo = VGroup(
                    Line(c_simb + P3(-0.14, -0.14), c_simb + P3(0.14, 0.14)).set_stroke(TQ, 2.6),
                    Line(c_simb + P3(-0.14, 0.14), c_simb + P3(0.14, -0.14)).set_stroke(TQ, 2.6),
                )
            lt = T(r"\vec\tau", 42, TQ).next_to(circ_s, RIGHT, buff=0.16)
            return VGroup(pol, sr, lr, sf, lf, circ_s, miolo, lt)

        vp = vivo(_des_paral)
        self.play(FadeIn(vp), run_time=0.6)

        self.gat("força ao longo da distância")
        self.play(phi_tr.animate.set_value(0.0), run_time=1.4)

        P1, ip1 = M(r"\vec F", r"\parallel", r"\vec r", r"\ \Rightarrow\ ", r"\vec\tau", "=", r"\vec 0", size=48)
        self.pilha.poe(P1)
        self.monta(P1, ip1, {}, rt=0.9)

        self.gat("trocar a ordem")
        self.play(phi_tr.animate.set_value(math.radians(55.0)), run_time=0.7)
        self.play(inv_tr.animate.set_value(-1.0), run_time=1.0)

        P2, ip2 = M(r"\vec r", r"\times", r"\vec F", "=", "-", r"\vec F", r"\times", r"\vec r", size=50)
        self.pilha.poe(P2)
        self.monta(P2, ip2, {}, rt=1.0)
        self.foco = P2
        self.ate(0.99)

        # ── T2-4: componentes no plano xy: τ_z = x F_y − y F_x e teste na chave de roda ──
        self.an("T2-4")
        vp.clear_updaters()
        self.pilha.limpa()
        self.play(FadeOut(VGroup(vp, cab_t2, Ab, l_b, P1, P2)), run_time=0.45)

        # Eixos x, y na esquerda com chave de roda ao longo de +x
        O_xy = P3(-5.6, -0.55)
        eixo_x = Arrow(O_xy + LEFT * 0.4, O_xy + RIGHT * 4.2, buff=0, stroke_width=2.6, tip_length=0.18).set_color(GEO)
        eixo_y = Arrow(O_xy + DOWN * 1.2, O_xy + UP * 2.4, buff=0, stroke_width=2.6, tip_length=0.18).set_color(GEO)
        lx = T("x", 36, GEO).next_to(eixo_x.get_end(), DOWN, buff=0.16)
        ly = T("y", 36, GEO).next_to(eixo_y.get_end(), LEFT, buff=0.16)

        ch_xy = chave_roda(O_xy, comp=2.8, ang=0.0, cano=False)
        p_ap = ch_xy.ponta
        s_fx = seta(p_ap, p_ap + RIGHT * 0.95, FC, 5, tip=0.18, op=0.55)
        l_fx = T("F_x", 36, FC).next_to(s_fx, DOWN, buff=0.14)
        s_fy = seta(p_ap, p_ap + UP * 1.45, FC, 6, tip=0.20)
        l_fy = T("F_y", 36, FC).next_to(s_fy, LEFT, buff=0.14)
        cota_x = nm(r"x = 0{,}40\ \mathrm{m}", GEO, 36).move_to(O_xy + P3(1.4, -0.55))
        cota_y = nm(r"y = 0", GEO, 36).move_to(O_xy + P3(1.4, -1.00))

        C1, ic1 = M(r"\tau_z", "=", "x", "F_y", "-", "y", "F_x", size=54)
        Cb = caixa_l(C1, TQ)
        self.pilha.poe(Cb)
        self.play(FadeIn(eixo_x), FadeIn(eixo_y), FadeIn(lx), FadeIn(ly), FadeIn(ch_xy), FadeIn(s_fx), FadeIn(l_fx), FadeIn(s_fy), FadeIn(l_fy), FadeIn(cota_x), FadeIn(cota_y), run_time=0.8)
        self.cx(Cb[0])
        self.monta(C1, ic1, {3: l_fy, 6: l_fx}, rt=1.1)
        self.gat("coordenada x da posição vezes a parte vertical")

        # Na chave de roda: F_x = 0, F_y = 250 N
        self.gat("testa com a chave de roda")
        self.play(FadeOut(s_fx), FadeOut(l_fx), Transform(l_fy, nm(r"250\ \mathrm{N}", FC, 36).next_to(s_fy, RIGHT, buff=0.14)), run_time=0.6)

        C2, ic2 = M(r"\tau_z", "=", "0{,}40", r"\cdot", "250", "-", "0", "=", "+100", r"\,\mathrm{N\cdot m}", size=46)
        self.pilha.poe(C2)
        self.monta(C2, ic2, {2: cota_x, 4: l_fy, 6: cota_y}, rt=1.1)
        self.foco = C2
        self.ate(0.99)

        # ── T2-5: o torque depende do ponto escolhido (O na porca vs P no meio da chave) ──
        self.an("T2-5")
        self.pilha.limpa()
        cab_t25 = txt("DEPENDE DO PONTO ESCOLHIDO:", 26, bold=True, color=TQ)
        self.pilha.poe(cab_t25)
        self.play(FadeOut(VGroup(eixo_x, eixo_y, lx, ly, cota_x, cota_y, Cb, C2)), FadeIn(cab_t25), run_time=0.45)

        p_O = ch_xy.porca
        p_P = ch_xy.meio
        dot_O = Dot(p_O, radius=0.09, color=TQ).set_z_index(18)
        lbl_O = T("O", 40, TQ).next_to(dot_O, UP, buff=0.28)
        dot_P = Dot(p_P, radius=0.09, color=VETC).set_z_index(18)
        lbl_P = T("P", 40, VETC).next_to(dot_P, UP, buff=0.28)

        cota_O = VGroup(
            Line(p_O + 0.55 * DOWN, p_ap + 0.55 * DOWN).set_stroke(TQ, 2.6),
            nm(r"r_O = 0{,}40\ \mathrm{m}", TQ, 36).move_to((p_O + p_ap) / 2 + 0.90 * DOWN),
        )
        cota_P = VGroup(
            Line(p_P + 1.35 * DOWN, p_ap + 1.35 * DOWN).set_stroke(VETC, 2.6),
            nm(r"r_P = 0{,}20\ \mathrm{m}", VETC, 36).move_to((p_P + p_ap) / 2 + 1.70 * DOWN),
        )

        self.gat("a partir do parafuso")
        self.play(FadeIn(dot_O), FadeIn(lbl_O), FadeIn(cota_O), run_time=0.7)

        D1, id1 = M(r"\tau_O", "=", "0{,}40", r"\cdot", "250", "=", "100", r"\,\mathrm{N\cdot m}", size=50)
        self.pilha.poe(D1)
        self.monta(D1, id1, {2: cota_O[1], 4: l_fy}, rt=1.0)

        self.gat("a partir do meio da chave")
        self.play(FadeIn(dot_P), FadeIn(lbl_P), FadeIn(cota_P), run_time=0.7)

        D2, id2 = M(r"\tau_P", "=", "0{,}20", r"\cdot", "250", "=", "50", r"\,\mathrm{N\cdot m}", size=50)
        self.pilha.poe(D2)
        self.monta(D2, id2, {2: cota_P[1], 4: l_fy}, rt=1.0)

        D3, id3 = M(r"\tau_O", r"\neq", r"\tau_P", size=54)
        self.pilha.poe(D3)
        self.gat("nunca fala o torque dessa força")
        self.monta(D3, id3, {0: mp(D1, id1, [0]), 2: mp(D2, id2, [0])}, rt=0.9)
        self.selo("REGRA DE OURO", "SEMPRE DIGA: TORQUE EM RELAÇÃO A QUAL PONTO")
        self.foco = D3
        self.ate(0.99)
