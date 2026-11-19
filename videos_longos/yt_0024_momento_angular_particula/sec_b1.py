"""Lote PB1: B1 — DE p PARA L (Three.js 'mesa_furo' em C_34 na coluna esquerda; dolly para C_L em B1-3 e de volta em B1-4).
Fio removido; o disco congelado a 0,50 m do furo com p⃗ anti-horário (φ = 65° entre r⃗ e p⃗, L⃗ para cima). Todas as setas, o paralelogramo,
o ângulo, o braço e L⃗ são do Manim, presos à mesa pela projeção da câmera (pecas24.proj = mesa.js)."""
from pecas24 import *  # noqa: F401,F403

TH_D = -25 * RAD          # posição angular do disco
RD = 0.50
PHI = 65 * RAD            # ângulo entre r⃗ e p⃗
LP = 0.36                 # comprimento desenhado de p⃗ (m na mesa; sem escala numérica neste bloco)
LV = 0.30                 # v⃗ (desenho)


class LoteB1(Lote24):
    def corpo(self):
        self.camA = self.camB = C34B1
        self.fio = False
        self.rastro_on = False
        D = (RD * math.cos(TH_D), RD * math.sin(TH_D))
        self.mov = lambda tf: D
        self.anda(0.0, tf=0.0)
        f3 = self.mesa()
        dp = np.array([math.cos(TH_D + PHI), math.sin(TH_D + PHI), 0.0])
        D3 = np.array([D[0], D[1], 0.012])
        O3 = np.array([0.0, 0.0, 0.006])

        def r_seta():
            return etiqueta_vec(vetor_lab(self.tela(O3), self.tela(D3), VETC), "r", ref=lambda: self.tela(O3), part=lambda: self.tela(D3))      # v5: r⃗ do furo ao disco

        def p_seta():
            return etiqueta_vec(vetor_lab(self.tela(D3), self.tela(D3 + LP * dp), MAG), "sentido", ref=lambda: self.tela(D3 + dp) - self.tela(D3), nome="p⃗ B1")

        def paral():
            pts = [self.tela(O3), self.tela(D3), self.tela(D3 + LP * dp), self.tela(O3 + LP * dp)]
            return Polygon(*pts).set_fill(GEO, 0.22).set_stroke(GEO, 1.6, opacity=0.8).set_z_index(6)

        def rot_r():
            a, b = self.tela(O3), self.tela(D3)
            n = np.array([-(b - a)[1], (b - a)[0], 0]); n /= np.linalg.norm(n)
            if (np.dot(n, self.tela(D3 + LP * dp) - b) > 0) != getattr(self, "_r_lado", False):   # oposto ao paralelogramo (B1-2/3); no B1-4 oposto ao braço
                n = -n
            return T(r"\vec r", 44, VETC).move_to((a + b) / 2 + 0.42 * n)

        def rot_p():
            b = self.tela(D3 + LP * dp)
            return T(r"\vec p", 44, MAG).move_to(b + P3(0.35, 0.28))

        kL = ValueTracker(1.0)
        self.add(kL)

        def L_seta():
            k = max(0.02, float(kL.get_value()))
            return vetor_lab(self.tela(O3), self.tela(O3 + np.array([0, 0, 0.42 * k])), LMAG, origem=False)

        self.canto(txt("DE", 30), T("p", 40, MAG), txt("PARA", 30), T("L", 40, LMAG))

        # ── B1-1: retomada: p⃗ = m v⃗ · F⃗ = dp⃗/dt · cartão τ⃗ = r⃗ × F⃗ ──
        self.an("B1-1")
        f3.op.set_value(1.0)
        self.transicao(0.5)
        pd = self.tela(D3)
        s_v = vetor_lab(pd, self.tela(D3 + LV * dp), VEL)
        l_v = T(r"\vec v", 44, VEL).next_to(self.tela(D3 + LV * dp), UP, buff=0.18)
        l_m = T("m", 44, MAS).move_to(pd + P3(-0.05, -0.48))
        self.gat("o momento linear")
        self.play(FadeIn(s_v), FadeIn(l_v), FadeIn(l_m), run_time=0.6)
        A1, i1 = Mx(r"\vec p", "=", "m", r"\vec v")
        self.pilha.poe(A1)
        self.gat("a massa vezes a velocidade")
        self.lei(A1, i1, {2: l_m, 3: l_v})
        sp = vivo(p_seta)
        lp = vivo(rot_p)
        self.play(FadeOut(s_v), FadeOut(l_v), OpVivo(sp), OpVivo(lp), run_time=0.6)
        A2, i2 = Mx(r"\vec F", "=", r"\frac{d\vec p}{dt}")
        self.pilha.poe(A2)
        self.gat("a segunda lei de newton")
        self.lei(A2, i2, rt=1.2, metodo="lei")
        A3, i3 = Mx(r"\vec\tau", "=", r"\vec r", r"\times", r"\vec F")
        self.pilha.poe(A3)
        self.gat("lembra do torque")
        self.lei(A3, i3, rt=1.2, metodo="lei")
        self.ate(0.99)

        # ── B1-2: r⃗ do furo ao disco; paralelogramo; GM τ⃗ = r⃗ × F⃗ → L⃗ = r⃗ × p⃗ ──
        self.an("B1-2")
        self.gat("escolhe um ponto")
        anel_O = Circle(radius=0.2).move_to(self.tela(O3)).set_stroke(WHITE_, 2.6)
        l_O = T("O", 40, WHITE_).next_to(anel_O, LEFT, buff=0.15)
        self.play(Create(anel_O), FadeIn(l_O), run_time=0.6)
        self.gat("desenha o vetor posição")
        sr, lr = vivo(r_seta), vivo(rot_r)
        self.play(OpVivo(sr), OpVivo(lr), run_time=0.7)
        self.gat("faz o produto vetorial")
        pa = vivo(paral)
        self.play(OpVivo(pa), run_time=0.7)
        B, ib = Mx(r"\vec L", "=", r"\vec r", r"\times", r"\vec p")
        self.pilha.poe(B)
        self.gm(A3, B, (J(i3, 0), J(ib, 0)), (J(i3, 1), J(ib, 1)), (J(i3, 2), J(ib, 2)), (J(i3, 3), J(ib, 3)), (J(i3, 4), J(ib, 4)), rt=1.4)
        sub_B = self.resultado(B, LMAG)
        self.gat("isso tem nome")
        nome = txt("MOMENTO ANGULAR", 30, bold=True, color=LMAG).next_to(sub_B, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(nome), run_time=0.5)
        self.ate(0.99)

        # ── B1-3: dolly para C_L; L⃗ saindo do furo, perpendicular ao tampo; mão direita 2.5D ──
        self.an("B1-3")
        self.play(FadeOut(VGroup(anel_O, l_O)), FadeOut(l_m), run_time=0.4)
        self.dolly(CL, 1.6)
        self.gat("aponta para fora desse plano")
        # v2 §2.5: sem mão. Arco de varredura (branco, com ponta) gira de r⃗ para p⃗ no plano do tampo, em volta do furo, e L⃗ cresce junto
        RV = 0.22

        def varre():
            k = float(kL.get_value())
            if k < 0.02:
                return VGroup()
            pts = [self.tela(O3 + RV * np.array([math.cos(TH_D + a), math.sin(TH_D + a), 0])) for a in np.linspace(0, PHI * k, 24)]
            arco_ = VMobject().set_points_smoothly(pts).set_stroke(WHITE_, 4)
            u = pts[-1] - pts[-2]
            u = u / max(np.linalg.norm(u), 1e-6)
            nrm = np.array([-u[1], u[0], 0])
            pt = Polygon(pts[-1] + 0.16 * u, pts[-1] - 0.04 * u + 0.09 * nrm, pts[-1] - 0.04 * u - 0.09 * nrm).set_fill(WHITE_, 1).set_stroke(WHITE_, 1)
            return VGroup(arco_, pt).set_z_index(13)

        def giro():
            # ⟲ pequeno em perspectiva no pé de L⃗ (anti-horário visto de cima)
            k = float(kL.get_value())
            pts = [self.tela(O3 + np.array([0.07 * math.cos(a), 0.07 * math.sin(a), 0.05])) for a in np.linspace(-0.4, -0.4 + 4.8 * max(0.05, min(1, k)), 30)]
            c_ = VMobject().set_points_smoothly(pts).set_stroke(LMAG, 3)
            u = pts[-1] - pts[-2]
            u = u / max(np.linalg.norm(u), 1e-6)
            nrm = np.array([-u[1], u[0], 0])
            return VGroup(c_, Polygon(pts[-1] + 0.11 * u, pts[-1] + 0.06 * nrm, pts[-1] - 0.06 * nrm).set_fill(LMAG, 1).set_stroke(LMAG, 1)).set_z_index(14)
        kL.set_value(0.0)
        sL = vivo(L_seta)
        sv = vivo(varre)
        sg = vivo(giro)
        lL = vivo(lambda: T(r"\vec L", 46, LMAG).next_to(self.tela(O3 + np.array([0, 0, 0.42 * max(0.05, kL.get_value())])), LEFT, buff=0.35))
        self.add(sL, sv, sg, lL)
        self.play(kL.animate.set_value(1.0), run_time=1.6)
        self.gat("regra da mão direita")
        self.play(kL.animate.set_value(0.0), run_time=0.5)
        self.play(kL.animate.set_value(1.0), run_time=1.4)
        self.dolly(dict(CL, az=CL["az"] + 10.0), 1.0)          # §2.2: 1 s a mais girando 10° para o L⃗ ler como perpendicular
        self.gat("aqui ele aponta para cima")
        self.play(Indicate(B[0][0:2], color=LMAG, scale_factor=1.15), run_time=0.8)
        self.ate(0.99)

        # ── B1-4: volta a C_34; φ entre r⃗ e p⃗; braço r⊥ do furo até a reta de p⃗; |L⃗| = r p sen φ → (r sen φ) p → r⊥ p ──
        self.an("B1-4")
        self.play(OpVivo(sv, entra=False), OpVivo(sg, entra=False), OpVivo(sL, entra=False), OpVivo(lL, entra=False), OpVivo(pa, entra=False), run_time=0.4)
        self.remove(sL, lL, pa, sv, sg)
        self.pilha.so(B)
        self.play(FadeOut(nome), FadeOut(sub_B), run_time=0.3)
        self.dolly(C34B1, 1.6)
        self._r_lado = True
        # ângulo φ no disco: entre o prolongamento de r⃗ e p⃗
        er = np.array([math.cos(TH_D), math.sin(TH_D), 0.0])
        ext = vivo(lambda: DashedLine(self.tela(D3), self.tela(D3 + 0.32 * er), dash_length=0.08).set_stroke(VETC, 2.4, opacity=0.9))
        arco = vivo(lambda: VMobject().set_points_smoothly([self.tela(D3 + 0.16 * np.array([math.cos(TH_D + a), math.sin(TH_D + a), 0])) for a in np.linspace(0, PHI, 16)]).set_stroke(ANG, 4))
        l_phi = T(r"\varphi", 44, ANG).move_to(self.tela(D3 + 0.30 * np.array([math.cos(TH_D + PHI / 2), math.sin(TH_D + PHI / 2), 0])) + P3(0.55, -0.18))
        self.gat("o seno do ângulo")
        self.play(FadeIn(ext), FadeIn(arco), FadeIn(l_phi), run_time=0.6)
        C1, c1 = Mx(r"|\vec L|", "=", "r", "p", r"\operatorname{sen}\varphi")
        self.pilha.poe(C1)
        self.lei(C1, c1, {2: lr, 3: lp, 4: l_phi}, rt=1.2)
        # braço: pé da perpendicular do furo à reta de p⃗
        t_pe = float(-(D3 - O3) @ dp)
        PE = D3 + t_pe * dp
        self.gat("a distância vezes o seno")
        C2, c2 = Mx(r"|\vec L|", "=", "(", "r", r"\operatorname{sen}\varphi", ")", "p")
        self.pilha.poe(C2)
        self.gm(C1, C2, (J(c1, 0), J(c2, 0)), (J(c1, 1), J(c2, 1)), (J(c1, 2), J(c2, 3)), (J(c1, 4), J(c2, 4)), (J(c1, 3), J(c2, 6)), ([], J(c2, 2)), ([], J(c2, 5)))
        self.gat("exatamente este segmento")
        reta = DashedLine(self.tela(D3 + LP * dp), self.tela(PE - 0.10 * dp), dash_length=0.1).set_stroke(MAG, 2, opacity=0.75)
        braco = DashedLine(self.tela(O3), self.tela(PE), dash_length=0.1).set_stroke(VETC, 4)
        ret = angulo_reto(self.tela(PE), self.tela(O3), self.tela(PE + 0.1 * dp), s=0.16, cor=WHITE_)
        l_rp = T(r"r_\perp", 44, VETC).move_to((self.tela(O3) + self.tela(PE)) / 2 + P3(-0.75, 0.35))
        chave = Brace(VGroup(*[C2[0][j] for j in J(c2, 3, 4)]), DOWN, buff=0.06).set_color(VETC)
        self.play(Create(reta), Create(braco), FadeIn(ret), FadeIn(l_rp), FadeIn(chave), run_time=0.9)
        self.gat("é o braço igualzinho")
        C3, c3 = Mx(r"|\vec L|", "=", r"r_\perp", "p")
        self.pilha.poe(C3)
        self.gm(C2, C3, (J(c2, 0), J(c3, 0)), (J(c2, 1), J(c3, 1)), (J(c2, 2, 3, 4, 5), J(c3, 2)), (J(c2, 6), J(c3, 3)), rt=1.3, extra=(FadeOut(chave),))
        self.play(Indicate(braco, color=VETC, scale_factor=1.05), run_time=0.6)
        self.resultado(C3, LMAG)
        self.ate(0.99)

        # ── B1-5: unidade ──
        self.an("B1-5")
        self.pilha.so(B, C3)
        D1, d1 = Mx(r"[L]", "=", r"\mathrm{kg}", r"\cdot", r"\mathrm{m}", r"\cdot", r"\mathrm{m/s}")
        self.pilha.poe(D1)
        self.gat("vezes o braço")
        self.play(Indicate(braco, color=VETC, scale_factor=1.06), Indicate(l_rp, color=VETC), run_time=1.0)
        self.gat("por isso a unidade")
        self.lei(D1, d1, rt=1.3)
        D2, d2 = Mx("=", r"\mathrm{kg\,m^2/s}")
        self.pilha.poe(D2)
        self.gat("metro quadrado por segundo")
        self.lei(D2, d2, rt=0.9)
        self.ate(0.97)
        self.play(FadeOut(VGroup(reta, braco, ret, l_rp, ext, arco, l_phi)), OpVivo(sr, entra=False), OpVivo(lr, entra=False),
                  OpVivo(sp, entra=False), OpVivo(lp, entra=False), run_time=0.4)
