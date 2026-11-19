"""Lote PT4: T4 — AROS, DISCOS E ESFERAS. T4-1 aro (toda a massa a R) → MR²; T4-2 disco desmontado em anéis (dm = σ2πr dr) → ½MR²;
T4-3 aro × disco (mesma M e R; metade da massa do disco dentro de R/√2); T4-4 Three.js 'esfera': a esfera maciça se fatia em 14 discos
empilhados no eixo z; o disco na altura z (raio √(R² − z²), espessura dz) acende em rosa; z, raio e dz presos pelo Manim (projeta3d) → ⅖MR²;
T4-5 tabela I = cMR² (c em rosa) + a barra numa linha separada."""
from pecas21 import *  # noqa: F401,F403

C4, R4 = P3(-3.75, -0.35), 2.05
NE, KHI = 14, 10                                    # esfera: discos; o destacado (z = +0,357 R)


class LoteT4(Lote21):
    def corpo(self):
        self.an("T4-1")
        self.secao("AROS, DISCOS E ESFERAS")
        self.guia(['PERGUNTA:', 'E UM ARO, COM TODA A MASSA', 'NA BORDA?'])                                      # v6 G4: a coluna da direita não fica vazia
        aro = aro2d(C4, R4, 0.16)
        pts = VGroup(*[Dot(C4 + R4 * np.array([math.cos(a), math.sin(a), 0]), radius=0.08, color=MAS).set_z_index(9)
                       for a in np.linspace(0, 2 * PI, 16, endpoint=False)])
        raios = VGroup(*[DashedLine(C4, C4 + R4 * np.array([math.cos(a), math.sin(a), 0]), dash_length=0.07).set_stroke(GEO, 1.8, opacity=0.55)
                         for a in np.linspace(0, 2 * PI, 8, endpoint=False)]).set_z_index(3)
        ex = eixo_cruz(C4, 0.18)
        lR = T("R", 46).next_to(C4 + R4 * 0.5 * np.array([math.cos(0.4), math.sin(0.4), 0]), UP, buff=0.12)
        lM = T("M", 46).next_to(C4 + R4 * np.array([math.cos(2.4), math.sin(2.4), 0]), UL, buff=0.14)
        self.play(FadeIn(aro), FadeIn(ex), run_time=0.6)
        self.gat("e se o corpo é um aro")
        self.play(FadeIn(pts), FadeIn(lM), run_time=0.6)
        self.gat("cada pedaço está à mesma distância")
        self.play(Create(raios), FadeIn(lR), run_time=0.9)
        A, ia = M("I", "=", r"\sum", "m_i", "R^2", size=52)
        self.pilha.poe(A)
        self.gat("então a soma de m i r ao quadrado")
        self.monta(A, ia, {3: pts[3], 4: lR})
        B, ib = M("=", r"\Big(\sum m_i\Big)", "R^2", size=52)
        self.pilha.poe(B)
        self.gat("r ao quadrado vezes a soma das massas")
        self.passo(A, B, (J(ia, 1), J(ib, 0)), (J(ia, 4), J(ib, 2)), rt=1.2, origem=False)
        C_, ic = M("I", "=", "M", "R^2", size=56)
        Cb = caixa_l(C_, MAS)
        self.pilha.poe(Cb)
        self.gat("sem integral")
        self.cx(Cb[0])
        self.monta(C_, ic, {2: lM, 3: mp(B, ib, [2])})
        self.foco = Cb
        self.ate(0.99)
        # ── T4-2: disco em anéis ──
        self.an("T4-2")
        NA = 8
        disco = disco_aco(C4, R4)
        aneis = VGroup(*[Annulus(inner_radius=R4 * k / NA, outer_radius=R4 * (k + 1) / NA).move_to(C4).set_stroke(mix(MAS, 0.2), 1.6).set_fill(MAS, 0.18)
                         for k in range(NA)]).set_z_index(5)
        KA = 5
        anel = Annulus(inner_radius=R4 * KA / NA, outer_radius=R4 * (KA + 1) / NA).move_to(C4).set_stroke(WHITE_, 2.6).set_fill(MAS, 0.75).set_z_index(7)
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'E UM DISCO MACIÇO?'])                                      # v6 G4: a coluna da direita não fica vazia
        self.troca([aro, pts, raios, lR, lM], FadeIn(disco), seq=True)
        self.gat("corta em anéis finos")
        self.play(LaggedStart(*[FadeIn(a_, scale=0.96) for a_ in aneis], lag_ratio=0.15), run_time=1.4)
        exp_ = ValueTracker(0.0)
        self.add(exp_)
        aneis.add_updater(lambda g: [a_.scale_to_fit_width(2 * R4 * (k + 1) / NA * (1 + 0.04 * exp_.get_value() * k / NA)).move_to(C4) for k, a_ in enumerate(g)])
        self.play(exp_.animate(rate_func=there_and_back).set_value(1.0), run_time=1.0)
        aneis.clear_updaters()
        rr = R4 * (KA + 0.5) / NA
        lin_r = Line(C4, C4 + rr * np.array([math.cos(-0.5), math.sin(-0.5), 0])).set_stroke(GEO, 3).set_z_index(9)
        lr = T("r", 44).next_to(lin_r.get_end(), DR, buff=0.12)
        p_dr = C4 + R4 * np.array([math.cos(3.75), math.sin(3.75), 0])
        ldr = T("dr", 40).move_to(C4 + (R4 + 0.5) * np.array([math.cos(3.75), math.sin(3.75), 0]))      # v6 S4: fora do disco
        ldm = T(r"dm=\sigma\,2\pi r\,dr", 40).next_to(C4 + R4 * UP, UP, buff=0.12)
        self.gat("um anel de raio r")
        self.play(FadeIn(anel), Create(lin_r), FadeIn(lr), FadeIn(ldr), run_time=0.8)
        self.play(anel.animate(rate_func=there_and_back).scale(0.55, about_point=C4), run_time=2.2)      # o anel percorre os raios (a faixa cresce com r)
        self.play(anel.animate(rate_func=there_and_back).scale(1.0, about_point=C4), run_time=0.4)
        D_, id_ = M(r"\sigma", "=", r"\tfrac{M}{\pi R^2}", size=48)
        self.pilha.poe(D_)
        self.gat("massa a densidade por área")
        self.play(FadeIn(ldm, shift=0.08 * UP), FadeIn(D_), run_time=0.8)
        E_, ie = M("I", "=", r"\int_0^R", "r^2", r"\,\sigma\,2\pi r\,dr", size=50)
        self.pilha.poe(E_)
        self.gat("cada anel é um aro")
        self.monta(E_, ie, {3: lr, 4: ldm[0][3:]})
        F_, if_ = M("=", r"2\pi\sigma", r"\tfrac{R^4}{4}", "=", r"\tfrac{1}{2}", "M", "R^2", size=50)
        self.pilha.poe(F_)
        self.gat("integra de zero até r")
        self.passo(E_, F_, (J(ie, 1), J(if_, 0)), rt=1.2, origem=False)
        self.reg("t4_2", I_disco=0.5, aneis=NA)
        self.foco = F_
        self.ate(0.99)
        # ── T4-3: aro × disco ──
        self.an("T4-3")
        self.pilha.limpa(rt=0.3)
        CA, CD, RR = P3(-5.3, -0.4), P3(-1.85, -0.4), 1.45
        aro_b = aro2d(CA, RR, 0.13)
        d_b = VGroup(disco_aco(CD, RR), Circle(radius=RR / math.sqrt(2)).move_to(CD).set_stroke(width=0).set_fill(MAS, 0.8).set_z_index(5),
                     Annulus(inner_radius=RR / math.sqrt(2), outer_radius=RR).move_to(CD).set_stroke(width=0).set_fill(MAS, 0.3).set_z_index(5))
        meio = DashedVMobject(Circle(radius=RR / math.sqrt(2)).move_to(CD).set_stroke(WHITE_, 2.2), num_dashes=40).set_z_index(7)
        lme = txt("METADE DA MASSA · ¼ DE I", 24).next_to(d_b, DOWN, buff=0.55)
        l34 = txt("¾ DE I", 26, bold=True).next_to(d_b, UP, buff=0.5)
        la = txt("ARO", 26, bold=True).next_to(aro_b, DOWN, buff=0.2)
        self.troca([disco, aneis, anel, lin_r, lr, ldr, ldm, ex], FadeIn(aro_b), FadeIn(d_b), FadeIn(eixo_cruz(CA, 0.15)), FadeIn(eixo_cruz(CD, 0.15)), FadeIn(la), seq=True)
        G1, ig1 = M(r"I_{aro}", "=", "M", "R^2", size=52)
        G2, ig2 = M(r"I_{disco}", "=", r"\tfrac{1}{2}", "M", "R^2", size=52)
        self.pilha.poe(G1)
        self.pilha.poe(G2)
        self.gat("mesma massa mesmo raio")
        self.play(FadeIn(G1), FadeIn(G2), run_time=0.8)
        self.selo("O ARO TEM O DOBRO", "")
        self.vivos = [aro_b, d_b]
        for _ in range(2):
            self.play(Indicate(aro_b, scale_factor=1.05, color=WHITE_), Indicate(d_b, scale_factor=1.05, color=WHITE_), run_time=1.3)      # v6 parado 8:00
        angd = np.linspace(0, 2 * PI, 12, endpoint=False)                 # v6 §5: o aro "cede" massa ao miolo do disco
        pts_d = VGroup(*[Dot(CA + RR * np.array([math.cos(t_), math.sin(t_), 0]), radius=0.07, color=MAS).set_z_index(9) for t_ in angd])
        alvos_d = [CD + (RR / math.sqrt(2)) * (0.25 + 0.7 * ((k * 0.618) % 1)) * np.array([math.cos(k * 2.4), math.sin(k * 2.4), 0]) for k in range(12)]
        self.play(FadeIn(pts_d), run_time=0.4)
        self.play(LaggedStart(*[d_.animate.move_to(p_) for d_, p_ in zip(pts_d, alvos_d)], lag_ratio=0.18), Indicate(aro_b, scale_factor=1.04, color=WHITE_), Indicate(d_b, scale_factor=1.04, color=WHITE_), run_time=3.4)
        self.play(FadeOut(pts_d), run_time=0.4)
        self.gat("no disco metade da massa está dentro deste círculo")
        self.play(Create(meio), FadeIn(lme), GrowArrow(Arrow(lme.get_top(), CD + (RR / math.sqrt(2)) * DOWN + 0.05 * DOWN, buff=0.08, stroke_width=4, max_tip_length_to_length_ratio=0.35).set_color(WHITE_)), run_time=0.8)
        self.gat("ela responde por apenas um quarto")
        self.play(Indicate(lme, color=WHITE_, scale_factor=1.12), run_time=0.8)
        self.gat("os outros três quartos")
        self.play(FadeIn(l34), GrowArrow(Arrow(l34.get_bottom(), CD + RR * UP + 0.02 * UP, buff=0.08, stroke_width=4, max_tip_length_to_length_ratio=0.35).set_color(WHITE_)), self.ind_copia(d_b[2], MAS, 1.04, 0.9), run_time=0.9)
        self.gat("no aro toda a massa está na borda")
        self.play(self.ind_copia(aro_b, MAS, 1.04, 0.9), run_time=0.9)
        self.foco = G1
        self.ate(0.99)
        # ── T4-4: a esfera fatiada (Three.js) ──
        self.an("T4-4")
        self.sem_selo()
        self.pilha.limpa(rt=0.3)
        cut, sep, hio, rot_ = (ValueTracker(v) for v in (0.0, 0.0, 0.0, 0.0))
        self.add(cut, sep, hio, rot_)
        cam = cam_e()

        def est(t):
            e = r4({"cut": cut.get_value(), "sep": sep.get_value(), "hi": KHI if hio.get_value() > 0.01 else -1, "hiop": hio.get_value(),
                    "rot": rot_.get_value(), "eixos": 0, "cam": cam})
            if not PEDIDOS3D and e["hi"] >= 0:                 # alinhamento 3D × Manim: os mesmos pontos pela câmera do Manim (com o sep arredondado do estado)
                zk_ = -1 + (2.0 / NE) * (KHI + 0.5)
                self.reg("al_t44", centro=projeta3d(cam, (0, 0, zk_ * (1 + e["sep"]))), borda=projeta3d(cam, (math.sqrt(1 - zk_ ** 2), 0, zk_ * (1 + e["sep"]))))
            return e
        f3 = Fundo3D(self, "esfera", est, op=0.0)
        self.add(f3)
        velhos = [m for m in self.snap() if m not in (cut, sep, hio, rot_, f3)]
        self.troca(velhos, f3.op.animate.set_value(1.0), seq=True)
        self.guia(['PERGUNTA:', 'E UMA ESFERA MACIÇA,', 'FATIADA EM DISCOS?'])
        DZ = 2.0 / NE
        zk = -1 + DZ * (KHI + 0.5)
        rk = math.sqrt(1 - zk * zk)

        def pt(x, y, z):
            return projeta3d(cam, (x, y, z * (1 + sep.get_value())))
        self.gat("a gente fatia em discos finos")
        self.play(cut.animate.set_value(1.0), sep.animate.set_value(0.22), rot_.animate.set_value(0.3), run_time=1.6)
        self.play(hio.animate.set_value(1.0), run_time=0.5)
        # rótulos presos ao 3D (o eixo z, a altura z, o raio do disco e dz)
        DK_ = "#06102A"

        def halo(m, w=7):                                           # v6: texto e linhas sobre o 3D claro ganham contorno escuro (o z cinza sumia no disco branco)
            m.set_stroke(DK_, w, background=True)
            return m

        def lin_h(a, b, cor, w, dash=False):
            ln = DashedLine(a, b, dash_length=0.08) if dash else Line(a, b)
            ln.set_stroke(cor, w)
            ln.set_background_stroke(color=DK_, width=w + 5)
            return ln
        camadas = vivo(lambda: VGroup(
            lin_h(pt(0, 0, -1.25), pt(0, 0, 1.1), GEO, 2.4, dash=True),
            lin_h(pt(0, 0, zk), pt(rk, 0, zk), GEO, 3.2),
            Dot(pt(0, 0, zk), radius=0.06, color=GEO).set_background_stroke(color=DK_, width=4), Dot(pt(rk, 0, zk), radius=0.06, color=GEO).set_background_stroke(color=DK_, width=4)).set_z_index(12))
        lz = halo(T("z", 48))
        lz.add_updater(lambda m: m.next_to(pt(0, 0, zk / 2), LEFT, buff=0.35))
        lzl = vivo(lambda: VGroup(lin_h(pt(0, 0, 0), pt(0, 0, zk), GEO, 5)).set_z_index(13))
        hip_ = vivo(lambda: VGroup(lin_h(pt(0, 0, 0), pt(rk, 0, zk), WHITE_, 3.0, dash=True)).set_z_index(13))
        lrr = halo(T("r", 44))
        lrr.add_updater(lambda m: m.next_to(pt(rk / 2, 0, zk), UP, buff=0.12))
        lRR = halo(T("R", 46))
        lRR.add_updater(lambda m: m.next_to(pt(rk / 2, 0, zk / 2), DOWN, buff=0.25))
        lrad = halo(T(r"\sqrt{R^2-z^2}", 40))
        lrad.add_updater(lambda m: m.next_to(pt(rk, 0, zk), RIGHT, buff=0.2).shift(0.12 * UP))
        ldz = halo(T("dz", 44))
        ldz.add_updater(lambda m: m.next_to(pt(-rk, 0, zk), LEFT, buff=0.7))
        self.reg("esfera_t44", z=zk, r=rk, dz=DZ, n=NE, vols=[math.pi * (1 - (-1 + DZ * (k + 0.5)) ** 2) * DZ for k in range(NE)], vol_esfera=4 * math.pi / 3,
                 cam=list(map(str, cam.items())))
        self.gat("o disco na altura z")
        self.play(FadeIn(camadas), FadeIn(lzl), FadeIn(lz), run_time=0.7)
        self.gat("tem raio raiz de r ao quadrado menos z")
        self.add(lrr, lRR)                                          # v6: de onde vem a raiz — o triângulo retângulo da própria figura: r² + z² = R²
        self.play(FadeIn(hip_), FadeIn(lrr), FadeIn(lRR), run_time=0.8)
        P1, ip1 = M("r^2", "+", "z^2", "=", "R^2", size=50)
        P2, ip2 = M("r", "=", r"\sqrt{R^2-z^2}", size=50)
        self.pilha.poe(P1)
        self.monta(P1, ip1, {0: lrr[0][0][:1], 2: lz[0][0][:1], 4: lRR[0][0][:1]}, rt=1.4)
        self.pilha.poe(P2)
        self.passo(P1, P2, (J(ip1, 0), J(ip2, 0)), rt=1.3, origem=False)
        self.play(FadeOut(lrr), FadeOut(P1), FadeIn(lrad), run_time=0.7)
        self.remove(P1)
        self.pilha.tira(P1)
        self.pilha._reflow(self.pilha.linhas, 0.4)
        self.play(FadeIn(ldz), FadeOut(hip_), FadeOut(lRR), run_time=0.7)
        lrr.clear_updaters()
        lRR.clear_updaters()
        H1, ih1 = M("dm", "=", r"\rho\,\pi", r"(R^2-z^2)", r"\,dz", size=48)
        self.pilha.poe(H1)
        self.monta(H1, ih1, {3: lrad, 4: ldz})
        H2, ih2 = M("dI", "=", r"\tfrac{1}{2}", "dm", r"(R^2-z^2)", size=48)
        self.pilha.poe(H2)
        self.gat("o momento de inércia a gente já sabe")
        self.monta(H2, ih2, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        H3, ih3 = M(r"\rho", "=", r"\tfrac{M}{\frac{4}{3}\pi R^3}", size=44)
        self.pilha.poe(H3, dx=0.4)
        H4, ih4 = M("I", "=", r"\tfrac{1}{2}\rho\pi\!\int_{-R}^{R}", r"(R^2-z^2)^2", r"\,dz", size=46)
        H5, ih5 = M("I", "=", r"\tfrac{2}{5}", "M", "R^2", size=56)
        H4b = caixa_l(H5, MAS)
        self.gat("integra de menos r até r")
        self.monta(H3, ih3, {}, rt=0.6)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.pilha.poe(H4)
        self.pilha.poe(H4b)
        self.monta(H4, ih4, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.play(rot_.animate.set_value(0.6), run_time=1.0)
        self.gat("dá dois quintos de m r ao quadrado")
        self.cx(H4b[0])
        self.monta(H5, ih5, {}, rt=0.8)                                  # v9: idem
        self.play(rot_.animate.set_value(0.8), run_time=0.8)
        self.foco = H4b
        self.al_pts = pt
        self.play(rot_.animate.set_value(1.1), run_time=max(0.5, self.resta() - 0.5))
        self.ate(0.99)
        # ── T4-5: tabela ──
        self.an("T4-5")
        for m in (lz, lrad, ldz):
            m.clear_updaters()
        camadas.clear_updaters()
        lzl.clear_updaters()
        self.pilha.limpa(rt=0.3)
        self.troca([camadas, lzl, lz, lrad, ldz], f3.op.animate.set_value(0.0), seq=True)
        self.remove(f3)
        linhas = [(self.ic_aro(), "ARO · CILINDRO OCO DE PAREDE FINA", "1"), (self.ic_casca(), "CASCA ESFÉRICA FINA", r"\tfrac{2}{3}"),
                  (self.ic_disco(), "DISCO · CILINDRO MACIÇO", r"\tfrac{1}{2}"), (self.ic_esfera(), "ESFERA MACIÇA", r"\tfrac{2}{5}")]
        rows = VGroup()
        for ic_, nome, c in linhas:
            ic_.scale_to_fit_height(0.62)
            rows.add(VGroup(ic_, txt(nome, 26), MathTex("c=" + c, font_size=46, color=MAS)))
        for r_ in rows:
            r_[0].move_to(P3(-5.6, 0))
            r_[1].move_to(P3(-4.95 + r_[1].width / 2, 0))
            r_[2].move_to(P3(1.75 + r_[2].width / 2, 0))
        rows.arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        cab = VGroup(txt("I =", 30, bold=True), MathTex("c", font_size=50, color=MAS), MathTex("M", font_size=50, color=MAS), MathTex("R^2", font_size=50, color=GEO)).arrange(RIGHT, buff=0.12)
        barra = VGroup(self.ic_barra(), txt("BARRA FINA:", 26), T(r"\tfrac{ML^2}{12}", 44), txt("CENTRO ·", 24), T(r"\tfrac{ML^2}{3}", 44), txt("PONTA", 24)).arrange(RIGHT, buff=0.22)
        barra[0].scale_to_fit_width(1.0)
        tab = VGroup(cab, rows, barra).arrange(DOWN, buff=0.36, aligned_edge=LEFT).move_to(P3(-1.1, -0.95))
        cab.move_to(P3(tab.get_x(), cab.get_y()))
        fundo = RoundedRectangle(corner_radius=0.14, width=tab.width + 0.6, height=tab.height + 0.45).move_to(tab).set_fill(PANEL, 0.85).set_stroke(MAS, 2.4)
        fundo._fundo = fundo._caixa = True
        sepl = Line(P3(fundo.get_left()[0] + 0.25, barra.get_top()[1] + 0.18), P3(fundo.get_right()[0] - 0.25, barra.get_top()[1] + 0.18)).set_stroke(GEO, 1.6, opacity=0.6)
        topo_f, larg_f, cx_f = fundo.get_top()[1], fundo.width, fundo.get_center()[0]

        def fundo_ate(y_base):                                         # v6 S5: o painel cresce com as linhas (nunca nasce gigante e vazio)
            h_ = topo_f - y_base
            return RoundedRectangle(corner_radius=0.14, width=larg_f, height=h_).move_to(P3(cx_f, topo_f - h_ / 2)).set_fill(PANEL, 0.85).set_stroke(MAS, 2.4)
        fundo_cheio = fundo.copy()
        fundo.become(fundo_ate(cab.get_bottom()[1] - 0.25))
        fundo._fundo = fundo._caixa = True
        self.play(FadeIn(fundo), FadeIn(cab), run_time=0.6)
        for r_, fr in zip(rows, ("esses números formam uma tabela", "todos assumem corpos homogêneos", "e o aro e a casca esférica", "o fator na frente")):
            self.gat(fr)
            self.play(FadeIn(r_, shift=0.1 * RIGHT), Transform(fundo, fundo_ate(r_.get_bottom()[1] - 0.25)), run_time=0.6)
        self.selo("CORPOS HOMOGÊNEOS", ["EIXO DE SIMETRIA"])
        self.gat("a barra fica numa linha separada")
        self.play(Create(sepl), FadeIn(barra, shift=0.1 * RIGHT), Transform(fundo, fundo_cheio), run_time=0.7)
        self.foco = fundo
        self.ate(0.99)

    # ícones da tabela ──────────────────────────────────────────────────────────
    def ic_aro(self):
        return aro2d(ORIGIN, 0.5, 0.1)

    def ic_casca(self):
        return VGroup(Circle(radius=0.5).set_stroke(MAS, 4), Ellipse(width=1.0, height=0.3).set_stroke(MAS, 2, opacity=0.6))

    def ic_disco(self):
        return VGroup(disco_aco(ORIGIN, 0.5), Circle(radius=0.5).set_stroke(width=0).set_fill(MAS, 0.4))

    def ic_esfera(self):
        return VGroup(esfera_aco(0.5), Circle(radius=0.5).set_stroke(MAS, 2.4))

    def ic_barra(self):
        r = Rectangle(width=1.6, height=0.22)
        aco(r, 1.4)
        return VGroup(r, eixo_cruz(ORIGIN, 0.12))
