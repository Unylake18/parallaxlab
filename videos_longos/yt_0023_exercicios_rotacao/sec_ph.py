"""Lote PH: hook H1–H3 (carretel 3D), abertura A1–A3 (logo, agenda com 4 ícones, caixa de ferramentas) e o desafio da régua D1–D3 (régua 3D
do yt_0022 com massa M na ponta e a moeda em cima)."""
from pecas23 import *  # noqa: F401,F403
from icones25 import ic25

Z1, Z2 = -0.50, -0.72          # centro dos blocos em repouso (m, cena 3D)
XB1, XB2 = RC + 0.008, -(rc + 0.008)   # v2: blocos no ponto tangente do fio (raio do tambor + raio do fio)


class LotePH(Lote23):
    def corpo(self):
        self.hook()
        self.abertura()
        self.regua()

    # ── HOOK ────────────────────────────────────────────────────────────────────────────────────────────────────
    def hook(self):
        tc = ValueTracker(0.0)          # tempo físico do carretel (s)
        ucam = ValueTracker(0.0)
        trava = ValueTracker(1.0)
        flash = ValueTracker(0.0)
        self.add(tc, ucam, trava, flash)

        def cam():
            return cam_car(ucam.get_value(), K=4.3, yc=1.35)

        def est(t):
            th = car_th(tc.get_value())
            e = {"th": th, "trava": round(trava.get_value(), 3), "esp_flash": round(flash.get_value(), 3), "z1": Z1, "z2": Z2, "cam": cam()}
            if not PEDIDOS3D:
                c = cam()
                self.reg("carretel", th=th, eixo=pr(c, (0, 0, 0)), b1=pr(c, (XB1, 0.05, Z1 - RC * th)), b2=pr(c, (XB2, -0.085, Z2 + rc * th)))
            return r4(e)

        f3 = Fundo3D(self, "carretel", est)
        self.add(f3)
        self.f3 = f3

        def pb1():
            return pr(cam(), (XB1, 0.05, Z1 - RC * car_th(tc.get_value())))

        def pb2():
            return pr(cam(), (XB2, -0.085, Z2 + rc * car_th(tc.get_value())))

        rot = vivo(lambda: VGroup(lbl(r"6{,}0\ \mathrm{kg}", MAS, 36).next_to(pb1(), RIGHT, buff=0.6),
                                  lbl(r"10{,}0\ \mathrm{kg}", MAS, 36).next_to(pb2(), LEFT, buff=0.66)).set_z_index(20))

        # H1
        self.an("H1")
        self.secao("QUAL BLOCO DESCE?")
        self.selo("PERGUNTA", "QUAL DESCE?")
        self.play(FadeIn(rot), run_time=0.6)
        c1 = VGroup(lbl(r"6{,}0\ \mathrm{kg}", MAS, 46), txt("NO TAMBOR GRANDE", 30)).arrange(RIGHT, buff=0.24)
        c2 = VGroup(lbl(r"10{,}0\ \mathrm{kg}", MAS, 46), txt("NO TAMBOR PEQUENO", 30)).arrange(RIGHT, buff=0.24)
        self.gat("fios em sentidos opostos")
        c3 = txt("FIOS EM SENTIDOS OPOSTOS", 30, color=GEO)
        self.pilha.poe(c3)
        self.play(FadeIn(c3, shift=0.1 * UP), ucam.animate.set_value(0.12), flash.animate.set_value(1.0), run_time=1.2)
        self.play(ucam.animate.set_value(0.0), flash.animate.set_value(0.0), run_time=1.2)
        self.gat("seis quilos no grande")
        self.pilha.poe(c1)
        self.play(FadeIn(c1, shift=0.1 * UP), self.ind_copia(rot[0][0], None, 1.15, 0.7), run_time=0.7)
        self.gat("dez no pequeno")
        self.pilha.poe(c2)
        self.play(FadeIn(c2, shift=0.1 * UP), run_time=0.6)
        self.gat("apostou no mais pesado")
        c4 = VGroup(txt("APOSTA:", 30, bold=True, color=CYAN), lbl(r"10{,}0\ \mathrm{kg}", MAS, 46), lbl(r"\downarrow", MAS, 46), txt("?", 34, bold=True)).arrange(RIGHT, buff=0.18)
        self.pilha.poe(c4)
        self.play(FadeIn(c4, shift=0.1 * UP), run_time=0.6)
        self.ate(0.99)

        # H2: a trava sai; câmera lenta ×2 até o leve descer ~0,45 m; rastros; hold
        self.an("H2")
        self.selo("CÂMERA LENTA", "×2")
        self.pilha.limpa()
        self.play(trava.animate.set_value(0.0), FadeOut(VGroup(c1, c2, c3, c4)), run_time=0.6)
        t_fim = 0.55
        r1 = vivo(lambda: Line(pr(cam(), (RC, 0.05, Z1)), pb1()).set_stroke(RAST, 2.5, opacity=0.6).set_z_index(5))
        r2 = vivo(lambda: Line(pr(cam(), (-rc, -0.085, Z2)), pb2()).set_stroke(RAST, 2.5, opacity=0.6).set_z_index(5))
        self.add(r1, r2)
        self.play(tc.animate.set_value(t_fim), run_time=2 * t_fim, rate_func=linear)
        d1 = VGroup(lbl(r"6{,}0\ \mathrm{kg}", MAS, 46), lbl(r"\downarrow", ACC, 50), txt("DESCE", 34, bold=True, color=ACC)).arrange(RIGHT, buff=0.2)
        d2 = VGroup(lbl(r"10{,}0\ \mathrm{kg}", MAS, 46), lbl(r"\uparrow", ACC, 50), txt("SOBE", 34, bold=True, color=ACC)).arrange(RIGHT, buff=0.2)
        self.gat("o de seis quilos desce")
        self.pilha.poe(d1)
        self.play(FadeIn(d1, shift=0.1 * DOWN), run_time=0.6)
        self.gat("e o de dez sobe")
        self.pilha.poe(d2)
        self.play(FadeIn(d2, shift=0.1 * UP), run_time=0.6)
        self.gat("sem motor")
        d3 = txt("SEM MOTOR, SEM EMPURRÃO", 30, color=GEO)
        self.pilha.poe(d3)
        self.play(FadeIn(d3, shift=0.08 * UP), run_time=0.6)
        self.ate(0.99)

        # H3: a pergunta e três etiquetas perto dos objetos
        self.an("H3")
        self.sem_selo()
        perg = VGroup(txt("COMO O MAIS LEVE", 36, bold=True), txt("VENCE O MAIS PESADO?", 36, bold=True)).arrange(DOWN, buff=0.12)
        self.pilha.limpa(anims=[FadeOut(VGroup(d1, d2, d3))])
        self.pilha.poe(perg)
        self.play(FadeIn(perg, shift=0.1 * UP), run_time=0.7)
        c = cam()
        eixo = pr(c, (0, 0, 0))
        e_tq = txt("TORQUE", 30, bold=True, color=FC).move_to(eixo + P3(2.85, 1.3))
        e_in = VGroup(txt("MOMENTO DE", 22, bold=True, color=MAS), txt("INÉRCIA", 22, bold=True, color=MAS)).arrange(DOWN, buff=0.06).move_to(P3(-6.46, 1.5))                         # v6: fora do carretel (à esquerda, margem ≥ 12 px)
        e_vi = txt("VÍNCULO", 30, bold=True, color=GEO).move_to(eixo + P3(-2.55, -1.35))
        self.gat("geometria das forças")
        self.play(FadeIn(e_tq, shift=0.1 * LEFT), run_time=0.6)
        self.gat("inércia de quem gira")
        self.play(FadeIn(e_in, shift=0.1 * LEFT), run_time=0.6)
        self.gat("quatro problemas")
        self.play(FadeIn(e_vi, shift=0.1 * RIGHT), tc.animate.set_value(0.0), run_time=1.2)
        lin = VGroup(txt("4 PROBLEMAS", 32, bold=True, color=CYAN), txt("EQUAÇÕES + CONFERÊNCIA", 28, color=GEO)).arrange(DOWN, buff=0.1)
        self.pilha.poe(lin)
        self.play(FadeIn(lin, shift=0.1 * UP), run_time=0.6)
        self.gat("conferindo cada resultado")
        self.play(tc.animate.set_value(0.4), run_time=1.6, rate_func=linear)
        self.foco = lin
        self.ate(0.99)
        self._h_sai = [f3, rot, r1, r2, e_tq, e_in, e_vi, perg, lin, tc, ucam, trava, flash]

    # ── ABERTURA ────────────────────────────────────────────────────────────────────────────────────────────────
    def abertura(self):
        self.an("A1")
        self.secao(None)
        self.play(*[FadeOut(m) for m in self._h_sai if not isinstance(m, (ValueTracker, Fundo3D))], self.f3.op.animate.set_value(0.0), run_time=0.45)
        for m in self._h_sai:
            m.clear_updaters()
        self.remove(*self._h_sai)
        self.pilha.linhas = []
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        aneis = VGroup(*[Circle(radius=r).move_to(P3(0, 0.9)).set_stroke(VEL, 2.2, opacity=o) for r, o in ((2.1, 0.35), (2.45, 0.2))])
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 34, bold=True).move_to(P3(0, -2.3))
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), run_time=0.8)
        self.play(aneis.animate.scale(1.06), run_time=max(0.5, self.resta() - 0.3))
        self.ate(0.99)

        # A2: título + NESTE VÍDEO + 4 ícones
        self.an("A2")
        tt = VGroup(txt("DINÂMICA DA ROTAÇÃO:", 40, bold=True), txt("4 PROBLEMAS EM QUE O MOMENTO DE INÉRCIA DECIDE TUDO", 28, bold=True)).arrange(DOWN, buff=0.16).move_to(P3(0, 2.45))
        nv = txt("NESTE VÍDEO:", 32, bold=True, color=CYAN).move_to(P3(-5.6, 0.95))
        xs = (-5.4, -1.8, 1.8, 5.4)
        nomes = ("O VOLANTE", "A HASTE E O EIXO", "O CARRETEL", "O PÊNDULO MAIS RÁPIDO")
        ics = VGroup()
        for k in range(4):
            ic = ic25(k, ORIGIN)
            ic.scale(min(2.4 / ic.width, 2.2 / ic.height)).move_to(P3(xs[k], -0.75))
            rt_ = txt(nomes[k], 26, bold=True).move_to(P3(xs[k], -2.55))
            g = VGroup(ic, rt_)
            escala_op(ic, 0.6)                                   # v8: só o desenho fica apagado até a sua vez; o título entra a 100%
            ics.add(g)
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(bv), run_time=0.35)
        self.play(FadeIn(tt, shift=0.1 * UP), FadeIn(nv), FadeIn(ics), run_time=0.8)
        self.secao("NESTE VÍDEO")
        ul = VGroup()
        for k, frase in enumerate(("primeiro um volante", "depois uma haste", "em seguida o carretel", "e por fim um pêndulo de disco")):
            self.gat(frase)
            novo = ics[k].copy()
            for x in novo.family_members_with_points():
                x.set_opacity(1.0) if not isinstance(x, VMobject) else (x.set_stroke(opacity=1.0, family=False), x.set_fill(opacity=1.0 if x.get_fill_opacity() > 0.01 else 0.0, family=False))
            ul.add(Line(P3(xs[k] - 1.3, -2.9), P3(xs[k] + 1.3, -2.9)).set_stroke(CYAN, 3.5))
            self.play(Transform(ics[k], novo), Create(ul[-1]), run_time=0.7)
        self.gat("o mais rápido possível")
        self.play(Indicate(ics[3][0], color=None, scale_factor=1.06), run_time=0.9)
        self.ate(0.99)

        # A3: caixa de ferramentas — disco girando à esquerda, cinco cartões à direita, cada um com sua marca no disco
        self.an("A3")
        self.secao("CAIXA DE FERRAMENTAS")
        self.play(FadeOut(VGroup(tt, nv, ics, ul)), run_time=0.35)
        C = P3(-3.85, -0.35)
        RD = 2.2
        ang = ValueTracker(0.0)
        ang.add_updater(lambda m, dt: m.increment_value(0.35 * dt))
        self.add(ang)
        marcas = {}

        camA = {"modo": "frente", "K": RD / 0.10, "xc": float(C[0]), "yc": float(C[1]), "camx": 0.0, "camz": 0.0, "fov": 14}

        def estA(t):
            return r4({"p": [[0.0, 0.0, 0.0, -ang.get_value(), 0]], "garfo": 0, "cam": camA})

        fA = Fundo3D(self, "pendulo", estA, op=0.0)
        self.add(fA)

        def disco():
            a = ang.get_value()
            return VGroup(Line(C + 0.3 * np.array([math.cos(a), math.sin(a), 0]), C + RD * 0.92 * np.array([math.cos(a), math.sin(a), 0])).set_stroke(WHITE_, 4)).set_z_index(6)

        dv = vivo(disco)
        disc_a = VGroup(Circle(radius=RD).move_to(C).set_fill(AÇO_FRIO, 1).set_stroke(AÇO_ARESTA, 3.5),
                        Circle(radius=RD * 0.9).move_to(C).set_fill("#2B3A55", 1).set_stroke(AÇO_ARESTA, 1.5, opacity=0.4),
                        *[Circle(radius=RD * f).move_to(C).set_stroke(AÇO_ARESTA, 1.4, opacity=0.3) for f in (0.7, 0.5)],
                        Circle(radius=0.28).move_to(C).set_fill("#1B2742", 1).set_stroke(AÇO_ARESTA, 2.0), Dot(C, radius=0.06, color=GEO_CL)).set_z_index(4)
        self.play(FadeIn(disc_a), FadeIn(dv), run_time=0.6)
        cards = []
        y0 = 2.2

        def cartao_(partes, cores=None):
            A, ia = M(*partes, size=46, cores=cores)
            return A, ia

        specs = [
            ("o momento de inércia a soma", (r"I", "=", r"\sum", "m", "r^2"), {3: MAS, 4: C_RAIO}),
            ("o teorema dos eixos paralelos", (r"I", "=", r"I_{cm}", "+", "M", "D^2"), {4: MAS, 5: C_RAIO}),
            ("a segunda lei da rotação", (r"\sum", r"\tau_{ext}", "=", "I", r"\alpha"), None),
            ("a energia cinética de rotação", ("K", "=", r"\tfrac{1}{2}", "I", r"\omega^2"), None),
            ("e as pontes entre o giro", ("v", "=", r"\omega", "r", r"\quad", "a_t", "=", r"\alpha", "r", r"\quad", "a_c", "=", r"\omega^2", "r"), {3: C_RAIO, 8: C_RAIO, 13: C_RAIO}),
        ]
        for k, (fr, partes, cores) in enumerate(specs):
            self.gat(fr)
            A, ia = M(*partes, size=44 if k == 4 else 48, cores=cores)
            bx = caixa_l(A, (MAS, MAS, FC, KC, VEL)[k])
            self.pilha.poe(bx)
            self.cx(bx[0])
            # marca no disco
            a = ang.get_value()
            if k == 0:
                mk = VGroup(*[VGroup(Line(C, C + rr * np.array([math.cos(t_), math.sin(t_), 0])).set_stroke(HALO, 9),
                                     Line(C, C + rr * np.array([math.cos(t_), math.sin(t_), 0])).set_stroke(C_RAIO, 4.5),
                                     Dot(C + rr * np.array([math.cos(t_), math.sin(t_), 0]), radius=0.13, color=HALO),
                                     Dot(C + rr * np.array([math.cos(t_), math.sin(t_), 0]), radius=0.09, color=MAS))
                              for rr, t_ in ((0.8, 2.3), (1.6, 3.6), (1.9, 5.2))])
                mk.add(VGroup(pilula(lbl("r", C_RAIO, 38).move_to(C + 1.05 * np.array([math.cos(3.6), math.sin(3.6), 0]) + 0.3 * UP), C_RAIO, 0.08),
                              lbl("r", C_RAIO, 38).move_to(C + 1.05 * np.array([math.cos(3.6), math.sin(3.6), 0]) + 0.3 * UP).set_z_index(17)))
            elif k == 1:
                p2 = C + P3(1.2, 0.0)
                mk = VGroup(eixo_cruz(p2, 0.14, MAS), DashedLine(C, p2, dash_length=0.1).set_stroke(C_RAIO, 4.5), lbl("D", C_RAIO, 40).move_to((C + p2) / 2 + 0.42 * DOWN))
            elif k == 2:
                mk = VGroup(arco_torque(C, r=0.6, sentido=1, a0=0.3, amp=2.0, cor=FC), seta_curva(C, 0.95, 2.6, 1.6, ACC, 6, tip=0.22),
                            lbl(r"\tau", FC, 38).move_to(C + P3(0.35, 0.85)), lbl(r"\alpha", ACC, 38).move_to(C + P3(-1.2, 0.75)))
            elif k == 3:
                mk = VGroup(barra_h(C[0] - 1.6, C[1] - RD - 0.55, 3.2, 0.7, KC), lbl("K", KC, 36).move_to(P3(C[0] - 1.95, C[1] - RD - 0.55)))
            else:
                pt_ = C + RD * np.array([math.cos(0.7), math.sin(0.7), 0])
                tg = np.array([-math.sin(0.7), math.cos(0.7), 0])
                mk = VGroup(Dot(pt_, radius=0.09, color=WHITE_), seta_s(pt_, pt_ + 1.0 * tg, VEL, 6), seta_s(pt_, pt_ - 0.9 * (pt_ - C) / RD, ACC, 6),
                            lbl("v", VEL, 36).move_to(pt_ + 1.0 * tg + 0.3 * RIGHT), lbl("a_c", ACC, 36).move_to(pt_ - 0.45 * (pt_ - C) / RD + 0.4 * DOWN + 0.25 * RIGHT))
            mk.set_z_index(12)
            velhas = [m for m in marcas.values()]
            marcas.clear()
            self.monta(A, ia, {}, rt=1.0)
            self.play(FadeIn(mk), *[FadeOut(m) for m in velhas], run_time=0.5)
            if k in (0, 1):                                  # v4 §1.2 #5: o r / D da fórmula e a linha do desenho pulsam juntos
                self.play(Indicate(mp(A, ia, [4 if k == 0 else 5]), color=None, scale_factor=1.25), Indicate(mk[0] if k == 0 else mk[1], color=None, scale_factor=1.08), run_time=0.7)
            marcas[k] = mk
        self.gat("então bora usar")
        self.play(*[FadeOut(m) for m in marcas.values()], run_time=0.4)
        self.foco = self.pilha.linhas[-1][0] if self.pilha.linhas else None
        self.ate(0.99)
        self._a_sai = [dv, ang, fA, disc_a]

    # ── O DESAFIO DA RÉGUA ──────────────────────────────────────────────────────────────────────────────────────
    def regua(self):
        cam = cam_reg()
        tf = ValueTracker(0.0)
        barras = ValueTracker(0.0)
        self.add(tf, barras)

        def est(t):
            e = estado_regua(tf.get_value(), massa_ponta=True)
            e["moeda_meio"] = False
            e["cam"] = cam
            e["barras"] = round(float(barras.get_value()), 4)
            e["hb"] = round(0.39 * (9 / 8) / 1.5, 5)
            if not PEDIDOS3D:
                th = e["th"]
                self.reg("regua", th=th, dob=tela_regua(cam, 0, th), meio=tela_regua(cam, 0.5, th), ponta=tela_regua(cam, 1.0, th))
            return r4(e)


        self.an("D1")
        self.secao("O DESAFIO DA RÉGUA")
        velhos = [m for m in self._a_sai if not isinstance(m, (ValueTracker, Fundo3D))]
        f_sai = [m for m in self._a_sai if isinstance(m, Fundo3D)]
        self.pilha.limpa(anims=[FadeOut(m) for m in velhos] + [m.op.animate.set_value(0.0) for m in f_sai])
        for m in self._a_sai:
            m.clear_updaters()
        self.remove(*self._a_sai)
        f3 = Fundo3D(self, "regua", est, op=0.0)
        self.add(f3)
        self.play(f3.op.animate.set_value(1.0), run_time=0.6)
        p_dob, p_meio, p_pt = [P3(*tela_regua(cam, r, 0.0), 0) for r in (0.0, 0.5, 1.0)]
        l_M = lbl("M", MAS, 42).move_to(p_pt + P3(0.5, 0.42))                  # v2 §5 #2: um rótulo M só, preso à massa da ponta
        moeda = txt("MOEDA", 30, bold=True, color=GEO).move_to(p_pt + P3(-0.75, 1.15))
        ch_m = Line(moeda.get_bottom() + 0.08 * DOWN, p_pt + P3(-0.1, 0.3)).set_stroke(GEO, 2)
        self.gat("uma moeda solta na ponta")
        self.play(FadeIn(moeda), Create(ch_m), run_time=0.6)
        self.gat("uma massa igual à da própria régua")
        self.play(FadeIn(l_M, shift=0.1 * DOWN), run_time=0.6)
        self.gat("a moeda é só detector")
        self.hip("MOEDA LEVE · DOBRADIÇA SEM ATRITO")
        self.gat("a ponta ainda passa da gravidade")
        q = VGroup(txt("A PONTA AINDA", 34, bold=True), linha_base([txt("ACELERA MAIS QUE", 34, bold=True), lbl("g", ACC, 50), txt("?", 34, bold=True)], 0.14)).arrange(DOWN, buff=0.14)
        self.pilha.poe(q)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)
        self.foco = q
        self.ate(0.99)

        # D2: Στ = Iα → τ (voos das setas e cotas) → I = Σ Iᵢ (cartão da haste + massa na ponta) → α = τ/I → cancelamentos → a_ponta = 9g/8
        self.an("D2")
        self.sem_selo()
        self.pilha.limpa(anims=[FadeOut(q), FadeOut(moeda), FadeOut(ch_m)])
        s1 = seta_s(p_meio + 0.12 * DOWN, p_meio + 1.25 * DOWN, FC, 6)
        s2 = seta_s(p_pt + 0.3 * DOWN, p_pt + 1.4 * DOWN, FC, 6)
        g1 = lbl("Mg", FC, 40).next_to(s1, LEFT, buff=0.16)
        g2 = lbl("Mg", FC, 40).next_to(s2, LEFT, buff=0.16)
        b1 = VGroup(Line(p_dob + 0.95 * UP, p_meio + 0.95 * UP).set_stroke(C_RAIO, 4.0), lbl(r"L/2", C_RAIO, 40).move_to((p_dob + p_meio) / 2 + 1.3 * UP))
        b2 = VGroup(Line(p_dob + 1.75 * UP, p_pt + 1.75 * UP).set_stroke(C_RAIO, 4.0), lbl("L", C_RAIO, 40).move_to((p_dob + p_pt) / 2 + 2.08 * UP))
        L0, i0, _ = self.lei("newton_rot", (r"\sum", r"\tau", "=", "I", r"\alpha"), rt=1.0)
        self.gat("o peso da régua no meio")
        self.play(FadeIn(s1), FadeIn(g1), FadeIn(b1), run_time=0.7)
        self.gat("o peso da massa extra na ponta")
        self.play(FadeIn(s2), FadeIn(g2), FadeIn(b2), run_time=0.7)
        A, ia, _ = self.linha((r"\tau", "=", "M", "g", r"\tfrac{L}{2}", "+", "M", "g", "L"),
                              voos={2: g1[0][0], 3: g1[0][1], 4: b1[1], 6: g2[0][0], 7: g2[0][1], 8: b2[1]}, rt=1.4)
        self.gat("somando três meios")
        A2, ia2, a2b = self.gm(A, ia, (r"\tau", "=", r"\tfrac{3}{2}", "M", "g", "L"), cores={2: FC}, caixa_cor=FC, rt=1.1)
        self.gat("um terço da massa")
        B0, ib0, _ = self.linha(("I", "=", r"\sum", "I_i"), rt=0.8)
        B, ib, _ = self.gm(B0, ib0, ("I", "=", r"\tfrac{1}{3}", "M", "L^2", "+", "M", "L^2"), sai=[2, 3], voos={6: l_M, 7: b2[1]}, rt=1.2)
        B2, ib2, b2b = self.gm(B, ib, ("I", "=", r"\tfrac{4}{3}", "M", "L^2"), cores={2: MAS}, caixa_cor=MAS, rt=1.0)
        self.gat("dividindo")
        self.pilha.so(L0, a2b, b2b, rt=0.5)
        C0, ic0, _ = self.gm(L0, i0, {"pre": (r"\alpha", "="), "num": (r"\tau",), "den": ("I",)}, sai=[0], rt=1.0)
        C, ic, _ = self.linha({"pre": (r"\alpha", "="), "num": (r"\tfrac{3}{2}", "M", "g", "L"), "den": (r"\tfrac{4}{3}", "M", "L^2")},
                              voos={2: mp(A2, ia2, [2]), 3: mp(A2, ia2, [3]), 4: mp(A2, ia2, [4]), 5: mp(A2, ia2, [5]),
                                    7: mp(B2, ib2, [2]), 8: mp(B2, ib2, [3]), 9: mp(B2, ib2, [4])}, rt=1.2)
        C2, ic2, c2b = self.gm(C, ic, {"pre": (r"\alpha", "="), "num": ("9", "g"), "den": ("8", "L")}, riscar=[3, 8, 5],
                             mapas=[([2], [2]), ([7], [5]), ([9], [6])], cores={2: ACC, 5: ACC}, caixa_cor=ACC, rt=1.2)
        self.gat("nove oitavos da gravidade")
        self.pilha.so(c2b, rt=0.4)
        D0, id0, _ = self.lei("pontes", (r"a_{\mathrm{ponta}}", "=", r"\alpha", "L"), voos={3: b2[1]}, rt=0.9)
        D1, id1, _ = self.linha({"pre": (r"a_{\mathrm{ponta}}", "="), "num": ("9", "g"), "den": ("8", "L"), "post": ("L",)},
                                voos={2: mp(C2, ic2, [2]), 3: mp(C2, ic2, [3]), 4: mp(C2, ic2, [4]), 5: mp(C2, ic2, [5]), 6: mp(C2, ic2, [6]), 7: b2[1]}, rt=1.1)
        D, idd, _ = self.gm(D1, id1, (r"a_{\mathrm{ponta}}", "=", r"\tfrac{9}{8}", "g"), riscar=[6, 7], mapas=[([2, 4, 5], [2])], cores={2: ACC}, caixa_cor=ACC, rt=1.1)
        self.foco = D
        self.ate(0.99)

        # D3: largada em câmera lenta; barra a(r) até 9g/8; marca 2L/3 → 8L/9
        self.an("D3")
        self.selo("CONFERE", [[lbl(r"\tfrac{9}{8}", ACC, 40), ">", "1", "· PASSA DE", lbl("g", ACC, 40)]])
        self.pilha.limpa(anims=[FadeOut(VGroup(s1, s2, g1, g2, b1, b2, l_M))])
        self.card_sai()
        self.play(barras.animate.set_value(1.0), run_time=1.0)
        xL = lambda r: p_dob[0] + (p_pt[0] - p_dob[0]) * r
        yb = p_dob[1] - 0.25
        lab_ant = lbl(r"\frac{2L}{3}", GEO, 40).move_to(P3(xL(2 / 3), yb - 2.75))
        marca_ant = VGroup(DashedLine(P3(xL(2 / 3), yb), P3(xL(2 / 3), yb - 2.35), dash_length=0.08).set_stroke(GEO, 2.5, opacity=0.5), lab_ant)
        self.gat("antes a ponta chegava")
        E, ie, _ = self.linha((r"\mathrm{antes}", ":", r"\tfrac{3}{2}", "g", r"\ \rightarrow\ ", r"\mathrm{agora}", ":", r"\tfrac{9}{8}", "g"), cores={2: ACC, 7: ACC}, size=46, rt=1.3)
        self.gat("o ponto da régua que acelera exatamente como a gravidade")
        self.play(FadeIn(marca_ant), run_time=0.6)
        marca_nova = VGroup(DashedLine(P3(xL(8 / 9), yb), P3(xL(8 / 9), yb - 2.35), dash_length=0.08).set_stroke(ACC, 3),
                            lbl(r"\frac{8L}{9}", ACC, 40).move_to(P3(xL(8 / 9), yb - 2.75)))
        self.gat("para oito nonos")
        self.play(ReplacementTransform(marca_ant.copy(), marca_nova), FadeOut(marca_ant), run_time=1.1)
        F0, if0, _ = self.linha(("a_t", "=", r"\alpha", "r", "=", "g"), rt=0.9)
        F, if_, _ = self.gm(F0, if0, ("r", "=", r"\frac{g}{\alpha}", "=", r"\tfrac{8}{9}", "L"), cores={4: GEO}, caixa_cor=GEO, sai=[0, 2, 1], rt=1.0)
        self.gat("primeira pista do vídeo")
        self.selo("CÂMERA LENTA", "×10 · A MOEDA FICA PARA TRÁS, MAS POUCO")
        self.play(barras.animate.set_value(0.0), FadeOut(marca_nova), run_time=0.4)
        self.play(tf.animate.set_value(0.15), run_time=min(4.0, max(1.5, self.resta() - 0.6)), rate_func=linear)
        self.foco = F
        self.ate(0.99)
        self.f3 = f3
