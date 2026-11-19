"""Lote PT2: T2 — DE QUE DEPENDE O MOMENTO DE INÉRCIA? Haltere 2D (duas massas de 2 kg numa haste leve de 1 m): eixo no meio, quadrados de lado r
sob cada massa (área ∝ r²) → I = 1 kg·m²; o eixo desliza até uma das massas (um quadrado some, o outro vira L × L) → 2 kg·m². T2-3: gráfico da
contribuição m r² × r (1 kg a 0,2 m e 0,25 kg a 0,4 m dão 0,04 cada; r → 2r multiplica por 4). T2-4: o haltere vira um anel de raio k (I = M k²)."""
from pecas21 import *  # noqa: F401,F403

YH, XC2, LS = 0.7, -3.6, 3.6                      # haste: altura, centro, comprimento na tela (1 m)
RB = 0.36


class LoteT2(Lote21):
    def corpo(self):
        self.an("T2-1")
        self.secao("DE QUE DEPENDE O MOMENTO DE INÉRCIA?")
        self.guia(['PERGUNTA:', 'O QUE MUDA O MOMENTO', 'DE INÉRCIA DO HALTERE?'], cor=MAS)
        xa = ValueTracker(XC2)                       # x do eixo na tela
        self.add(xa)
        c1, c2 = P3(XC2 - LS / 2, YH), P3(XC2 + LS / 2, YH)
        hal = haltere(c1, c2, RB)
        lm1 = VGroup(T("m=", 34), nm(r"2\ \mathrm{kg}", MAS, 34)).arrange(RIGHT, buff=0.08).next_to(c1, LEFT, buff=RB + 0.24)
        lm2 = VGroup(T("m=", 34), nm(r"2\ \mathrm{kg}", MAS, 34)).arrange(RIGHT, buff=0.08).next_to(c2, RIGHT, buff=RB + 0.24)

        def quadrados():
            x0 = xa.get_value()
            g = VGroup()
            for c in (c1, c2):
                r = abs(c[0] - x0)
                if r < 0.02:
                    continue
                q = Square(side_length=r).move_to(P3((c[0] + x0) / 2, YH - r / 2 - 0.0)).set_stroke(MAS, 2.5, opacity=0.9).set_fill(MAS, 0.22)
                g.add(q.set_z_index(3))
            g.add(eixo_cruz(P3(x0, YH), 0.2, z=14))
            return g
        qv = vivo(quadrados)
        cotaL = VGroup(Line(P3(c1[0], YH + 1.15), P3(c2[0], YH + 1.15)).set_stroke(GEO, 2.2),
                       Line(P3(c1[0], YH + 1.03), P3(c1[0], YH + 1.27)).set_stroke(GEO, 2.2), Line(P3(c2[0], YH + 1.03), P3(c2[0], YH + 1.27)).set_stroke(GEO, 2.2))
        lL = VGroup(T("L=", 40), nm(r"1\ \mathrm{m}", GEO, 40)).arrange(RIGHT, buff=0.08).next_to(cotaL, UP, buff=0.1)
        lm1.shift(0.0 * UP)
        self.play(FadeIn(hal), FadeIn(qv), run_time=0.7)
        self.gat("duas massas iguais de dois quilos")
        self.play(FadeIn(lm1), FadeIn(lm2), run_time=0.6)
        self.gat("haste leve de um metro")
        self.play(Create(cotaL[0]), FadeIn(cotaL[1:]), FadeIn(lL), run_time=0.6)
        lr1 = T(r"\tfrac{L}{2}", 44).next_to(P3((c1[0] + XC2) / 2, YH - LS / 2), DOWN, buff=0.14)
        lr2 = T(r"\tfrac{L}{2}", 44).next_to(P3((c2[0] + XC2) / 2, YH - LS / 2), DOWN, buff=0.14)
        self.gat("cada massa está a meio metro")
        self.play(FadeIn(lr1), FadeIn(lr2), run_time=0.6)
        A, ia = M("I", "=", "m", r"\big(\tfrac{L}{2}\big)^2", "+", "m", r"\big(\tfrac{L}{2}\big)^2", size=50)
        self.pilha.poe(A)
        self.gat("a conta é só somar")
        self.monta(A, ia, {2: lm1[0][0][:1], 3: lr1, 5: lm2[0][0][:1], 6: lr2})
        B, ib = M("=", r"\tfrac{1}{2}", "m", "L^2", size=50)
        self.pilha.poe(B)
        self.passo(A, B, (J(ia, 2), J(ib, 2)), rt=1.0, origem=False)
        C_, ic = M("I", "=", r"\tfrac{1}{2}", r"\cdot", "2", r"\cdot", "1^2", "=", r"1\ \mathrm{kg\cdot m^2}", size=50, cores={4: MAS, 6: GEO, 8: MAS})
        Cb = caixa_l(C_, MAS)
        self.pilha.poe(Cb)
        self.gat("dá um quilograma")
        self.cx(Cb[0])
        self.voa([(lm1[1][0][:1], mp(C_, ic, [4])), (lL[1][0][:1], mp(C_, ic, [6])[:1])], extra=[FadeIn(mp(C_, ic, [0, 1, 2, 3, 5, 7, 8])), FadeIn(mp(C_, ic, [6])[1:])],
                 rt=1.0, origem=False)
        self.reg("haltere_meio", I=2 * 2.0 * 0.5 ** 2)
        self.foco = Cb
        self.ate(0.99)
        # ── T2-2: o eixo desliza para uma das massas ──
        self.an("T2-2")
        self.play(FadeOut(lr1), FadeOut(lr2), run_time=0.3)
        self.gat("ele passa por uma das massas")
        self.play(xa.animate.set_value(c1[0]), run_time=2.0)
        lr3 = T("L", 44).next_to(P3(XC2, YH - LS), DOWN, buff=0.14)
        l0 = T(r"r=0", 40).next_to(c1, LEFT, buff=RB + 0.18).shift(0.8 * DOWN)
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'E SE O EIXO PASSAR', 'POR UMA DAS MASSAS?'], cor=MAS)
        D_, id_ = M("I", "=", "m", r"\cdot 0^2", "+", "m", "L^2", size=50)
        self.pilha.poe(D_)
        self.gat("uma massa fica em cima do eixo")
        self.play(FadeIn(l0), run_time=0.5)
        self.gat("a outra fica a um metro")
        self.play(FadeIn(lr3), run_time=0.5)
        self.monta(D_, id_, {2: lm1[0][0][:1], 5: lm2[0][0][:1], 6: lr3})
        self.play(Indicate(hal, scale_factor=1.05, color=WHITE_), run_time=1.3)                  # v6 parado 4:29: o haltere pulsa enquanto a fala fecha a conta
        self.play(Indicate(hal, scale_factor=1.05, color=WHITE_), run_time=1.3)
        E_, ie = M("I", "=", "m", "L^2", "=", "2", r"\cdot", "1^2", "=", r"2\ \mathrm{kg\cdot m^2}", size=50, cores={5: MAS, 7: GEO, 9: MAS})
        Eb = caixa_l(E_, MAS)
        self.pilha.poe(Eb)
        self.gat("o resultado é dois quilogramas")
        self.play(FadeIn(Eb[0]), FadeIn(mp(E_, ie, [0, 1, 2, 3, 4])), run_time=0.5)
        self.voa([(lm2[1][0][:1], mp(E_, ie, [5])), (lL[1][0][:1], mp(E_, ie, [7])[:1])], extra=[FadeIn(mp(E_, ie, [6, 8, 9])), FadeIn(mp(E_, ie, [7])[1:])],
                 rt=1.0, origem=False)
        self.reg("haltere_ponta", I=2.0 * 1.0 ** 2)
        self.selo("MESMO HALTERE, OUTRO EIXO", ["I DOBROU"])
        self.gat("e essa é a ideia mais importante")
        self.selo("IDEIA CENTRAL", [[T("I", 38), "DEPENDE DO EIXO"]])
        self.foco = Eb
        self.ate(0.99)
        # ── T2-3: o quadrado (gráfico m r² × r) ──
        self.an("T2-3")
        self.sem_selo()
        qv.clear_updaters()
        velhos = [hal, qv, lm1, lm2, cotaL, lL, lr3, l0]
        gr = Graf(-6.9, -2.75, 5.4, 0.5, 0, 0.25, 4.6 / 0.25, rot_y=T("m r^2", 40), rot_x="r", cor=GEO)
        cur1 = gr.curva(lambda r: 1.0 * r * r, 0, 0.47, cor=MAS, w=5)
        cur2 = gr.curva(lambda r: 0.25 * r * r, 0, 0.5, cor=mix(MAS, 0.45), w=4)
        l1 = VGroup(nm(r"1\ \mathrm{kg}", MAS, 36)).next_to(gr.pt(0.47, 0.2209), LEFT, buff=0.15)
        l2 = VGroup(nm(r"0{,}25\ \mathrm{kg}", MAS, 36)).next_to(gr.pt(0.5, 0.0625), UP, buff=0.15)
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'E SE O RAIO FOR O DOBRO?', 'O QUE ACONTECE COM O I?'], cor=MAS)
        self.troca(velhos, FadeIn(gr.eixos), seq=True)
        self.gat("se você afasta uma massa")
        self.play(Create(cur1), FadeIn(l1), run_time=1.0)
        p1, p1b = gr.pt(0.2, 0.04), gr.pt(0.4, 0.16)
        d1 = Dot(p1, radius=0.1, color=MAS).set_z_index(9)
        d1b = Dot(p1b, radius=0.1, color=MAS).set_z_index(9)
        sr = CurvedArrow(p1 + 0.12 * UR, p1b + 0.12 * LEFT, angle=-0.5).set_color(WHITE_).set_stroke(width=4)
        lx4 = T(r"r\to 2r:\ \times 4", 40).next_to(p1b, UL, buff=0.25)
        self.play(FadeIn(d1, scale=0.5), run_time=0.4)
        self.gat("a contribuição dela quadruplica")
        self.play(Create(sr), FadeIn(d1b), FadeIn(lx4), run_time=0.9)
        self.gat("uma massa pequena longe do eixo")
        self.play(Create(cur2), FadeIn(l2), run_time=0.9)
        p2 = gr.pt(0.4, 0.04)
        d2 = Dot(p2, radius=0.1, color=mix(MAS, 0.45)).set_z_index(9)
        hz = DashedLine(gr.pt(0, 0.04), p2, dash_length=0.08).set_stroke(MAS, 2.5, opacity=0.8)
        F1, if1 = M("1", r"\cdot", "0{,}2^2", "=", "0{,}04", size=48, cores={0: MAS, 2: GEO, 4: MAS})
        F2, if2 = M("0{,}25", r"\cdot", "0{,}4^2", "=", "0{,}04", size=48, cores={0: MAS, 2: GEO, 4: MAS})
        u1 = linha_m(F1, T(r"\mathrm{kg\cdot m^2}", 36, MAS), buff=0.12)
        u2 = linha_m(F2, T(r"\mathrm{kg\cdot m^2}", 36, MAS), buff=0.12)
        self.pilha.poe(u1)
        self.pilha.poe(u2)
        self.gat("pode pesar tanto quanto")
        self.play(FadeIn(d2), Create(hz), run_time=0.8)
        self.monta(F1, if1, {0: l1[0][0][:1], 2: d1}, rt=1.2)
        self.play(FadeIn(u1[1]), run_time=0.25)                    # v6 O4: a unidade só depois da conta
        self.gat("um quarto da massa")
        self.monta(F2, if2, {0: l2[0][0][:4], 2: d1b}, rt=1.2)
        self.play(FadeIn(u2[1]), run_time=0.25)
        self.reg("t2_3", c1=1.0 * 0.2 ** 2, c2=0.25 * 0.4 ** 2)
        self.foco = u2
        self.ate(0.99)
        # ── T2-4: raio de giração ──
        self.an("T2-4")
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'QUAL É O RAIO DE GIRAÇÃO', 'DE UM CORPO INTEIRO?'], cor=MAS)                                      # v6 G4: a coluna da direita não fica vazia
        C0 = P3(-3.75, -0.2)
        k_s = LS / 2
        mis = ValueTracker(0.0)
        self.add(mis)

        def anel():
            u = mis.get_value()
            g = VGroup()
            n = 24
            for q in range(n):
                lado = 0 if q < n // 2 else 1
                a_ini = PI if lado == 0 else 0.0
                a_fim = 2 * PI * q / n
                a = a_ini + (a_fim - a_ini) * u
                p = C0 + k_s * np.array([math.cos(a), math.sin(a), 0])
                g.add(Dot(p, radius=0.34 * (1 - u) + 0.09 * u, color=MAS).set_opacity(0.95 if u < 0.98 else 0.0).set_z_index(8))
            if u > 0.5:
                g.add(escala_op(aro2d(C0, k_s, 0.12), min(1.0, (u - 0.5) * 2)))
            if u < 0.98:
                g.add(Line(C0 + k_s * LEFT, C0 + k_s * RIGHT).set_stroke(GEO, 4, opacity=1 - u))
            g.add(eixo_cruz(C0, 0.18))
            return g
        av_ = vivo(anel)
        self.troca([gr.eixos, cur1, cur2, l1, l2, d1, d1b, sr, lx4, d2, hz], FadeIn(av_), seq=True)
        self.selo("RAIO DE GIRAÇÃO", [["ANEL COM O MESMO", T("I", 38)]])
        G_, ig = M("I", "=", "M", "k^2", size=56)
        Gb = caixa_l(G_, MAS)
        self.pilha.poe(Gb)
        self.gat("concentrando toda a massa num anel fino")
        self.play(mis.animate.set_value(1.0), run_time=2.2)
        av_.clear_updaters()
        rk = Line(C0, C0 + k_s * np.array([math.cos(0.6), math.sin(0.6), 0])).set_stroke(GEO, 3)
        lk = T("k", 46).next_to(rk.get_center(), UL, buff=0.08)
        lM = VGroup(T("M=", 40), nm(r"4\ \mathrm{kg}", MAS, 40)).arrange(RIGHT, buff=0.08).next_to(C0 + k_s * DOWN, DOWN, buff=0.3)
        self.play(Create(rk), FadeIn(lk), FadeIn(lM), run_time=0.7)
        self.gat("escreve i igual a massa total")
        self.cx(Gb[0])
        self.monta(G_, ig, {2: lM[0][0][:1], 3: lk})
        H_, ih = M("k", "=", r"\sqrt{\tfrac{I}{M}}", "=", r"\sqrt{\tfrac{1}{4}}", "=", r"0{,}5\ \mathrm{m}", "=", r"\tfrac{L}{2}", size=48, cores={4: WHITE_, 6: GEO})
        self.pilha.poe(H_)
        self.gat("no haltere são quatro quilos")
        self.play(FadeIn(mp(H_, ih, [0, 1, 2])), run_time=0.7)
        self.play(FadeIn(mp(H_, ih, [3, 4])), run_time=0.6)
        self.play(FadeIn(mp(H_, ih, [5, 6, 7, 8])), run_time=0.7)
        self.reg("t2_4", k=math.sqrt(1.0 / 4.0), k_cabo=NUM["k_cabo"], k_grossa=NUM["k_grossa"])
        self.foco = H_
        self.ate(0.99)
